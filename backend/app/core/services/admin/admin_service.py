from app.core.rag.rag_pipeline import RAG_Pipeline
from app.core.database.mysql_client import MysqlClient
from app.core.database.models import KnowledgeBase,UserInfo,Chat_Messages,Conversation
from app.core.rag.database.milvus.milvus_client import MilvusCollectionManager
from app.core.rag.database.elasticsearch.elastic_client import ElasticClient
from .admin_type import (SystemInfo,
                        UserConversation,
                        Conversation_Collection,
                        ConversationSession,
                        Message,
                        User_KnowledgeBase,
                        KnowledgeBaseItem,
                        KnowledgeBaseInfo
                         )
from typing import List,Tuple
from datetime import datetime
class AdminService:
    def __init__(self):
        pass
    
    # 获取系统基本信息
    def get_system_info(self)->SystemInfo:
        mysql_client = MysqlClient()
        # 获取知识库、用户、对话数量
        knowledge_base_count = mysql_client.db.query(KnowledgeBase).count()
        user_count = mysql_client.db.query(UserInfo).count()
        conversation_count = mysql_client.db.query(Conversation).count()
        
        return SystemInfo(
            knowledge_base_count=knowledge_base_count,
            user_count=user_count,
            conversation_count=conversation_count
        )
    
    # 获取用户对话信息
    def get_users_conversation(self) -> List[UserConversation]:
        mysql_client = MysqlClient()
        
        # 1. 首先获取所有用户
        users = mysql_client.db.query(UserInfo).all()
        user_conversation_list: List[UserConversation] = []

        # 2. 遍历每个用户
        for user in users:
            # 3. 获取该用户的所有对话
            conversations = mysql_client.db.query(Conversation).filter(
                Conversation.username == user.username
            ).all()
            
            conversation_collection: List[Conversation_Collection] = []
            
            # 4. 遍历该用户的所有对话
            for conversation in conversations:
                # 5. 获取该对话的所有消息
                chat_messages = mysql_client.db.query(Chat_Messages).filter(
                    Chat_Messages.conversationID == conversation.id
                ).all()
                
                # 6. 构建消息列表
                content: List[Message] = [
                    Message(
                        assistant=msg.answer,
                        message_time=msg.timeStamp,
                        user=msg.query
                    ) for msg in chat_messages
                ]
                
                # 7. 创建会话信息
                conversation_session = ConversationSession(
                    message_count=len(chat_messages),
                    content=content
                )
                
                # 8. 添加到会话集合
                conversation_collection.append(Conversation_Collection(
                    conversation_title=conversation.conversationName,
                    conversation_content=conversation_session,
                    conversation_time=str(conversation.lastChatTime),  # 转换为字符串
                    conversation_id=str(conversation.id)
                ))
            
            # 9. 为每个用户创建会话记录
            user_conversation_list.append(UserConversation(
                username=user.username,
                conversation_collection=conversation_collection
            ))
        
        return user_conversation_list
    
    # 获取所有用户创建的知识库
    def get_users_knowledge_base(self) -> List[User_KnowledgeBase]:
        mysql_client = MysqlClient()
        # 1. 首先获取所有用户
        users = mysql_client.db.query(UserInfo).all()
        user_KnowledgeBase: List[User_KnowledgeBase] = [] 
        # 2. 遍历每个用户
        for user in users:
            # 3. 获取该用户的所有知识库
            knowledge_bases = mysql_client.db.query(KnowledgeBase).filter(
                KnowledgeBase.created_by == user.username
            ).all()
            knowledge_base_list: List[KnowledgeBaseItem] = []
            # 4. 遍历该用户的所有知识库
            for knowledge_base in knowledge_bases:
                knowledge_base_info = KnowledgeBaseInfo(
                    knowledge_base_id=knowledge_base.knowledgeBaseId,
                    knowledge_base_name=knowledge_base.knowledgeBaseName,
                    docs_num=knowledge_base.docs_num,
                    words_num=knowledge_base.words_num,
                    related_conversations=knowledge_base.related_conversations,
                    delete_sign=knowledge_base.delete_sign,
                    create_time=knowledge_base.create_time,
                    update_time=knowledge_base.update_time,
                    created_by=knowledge_base.created_by
                )
                knowledge_base_list.append(KnowledgeBaseItem(
                    knowledge_base_id=knowledge_base.knowledgeBaseId,
                    knowledge_base_name=knowledge_base.knowledgeBaseName,
                    knowledge_base_info=knowledge_base_info
                ))
            user_KnowledgeBase.append(User_KnowledgeBase(
                knowledge_base_list=knowledge_base_list,
                username=user.username
            ))
        return user_KnowledgeBase
    
    # 删除用户对话
    def delete_user_conversation(self,username:str,conversation_id:int)->bool:
        mysql_client = MysqlClient()
        # 删除对话
        conversation = mysql_client.db.query(Conversation).filter(
            Conversation.username == username,
            Conversation.id == conversation_id
        ).first()
        
        conversation.delete_sign = True
        
        mysql_client.db.commit()
        
        mysql_client.db.refresh(conversation)
        
        return True
    
    # 删除用户知识库
    def delete_user_knowledge_base(self,username:str,knowledge_base_id:str)->bool:
        mysql_client = MysqlClient()
        # 删除知识库
        knowledge_base = mysql_client.db.query(KnowledgeBase).filter(
            KnowledgeBase.created_by == username,
            KnowledgeBase.knowledgeBaseId == knowledge_base_id
        ).first()
        
        knowledge_base.delete_sign = True
        
        mysql_client.db.commit()
        mysql_client.db.refresh(knowledge_base)
        
        try:
            milvus_client = MilvusCollectionManager()
            milvus_client.drop_collection(knowledge_base_id)
        except Exception as e:
            print(e)
        
        try:
            elastic_client = ElasticClient()
            elastic_client.delete_index(knowledge_base_id)
        except Exception as e:
            print(e)
        
        return True
    
    # 删除用户
    def delete_user(self,username:str)->bool:
        mysql_client = MysqlClient()
        # 删除用户
        user = mysql_client.db.query(UserInfo).filter(
            UserInfo.username == username
        ).first()
        
        user.delete_sign = True
        
        mysql_client.db.commit()
        mysql_client.db.refresh(user)
        
        return True
    
    # 授予用户管理员权限
    def grant_user_admin(self,username:str)->bool:
        mysql_client = MysqlClient()
        # 授予用户管理员权限
        user = mysql_client.db.query(UserInfo).filter(
            UserInfo.username == username
        ).first()
        user.is_admin = True
        mysql_client.db.commit()
        return True
    
    # 撤销用户管理员权限
    def revoke_user_admin(self,username:str)->bool:
        mysql_client = MysqlClient()
        # 撤销用户管理员权限
        user = mysql_client.db.query(UserInfo).filter(
            UserInfo.username == username
        ).first()
        if user.username == 'admin':
            return False
        
        if user.is_admin:
            user.is_admin = False
        
        mysql_client.db.commit()
        
        mysql_client.db.refresh(user)
        
        return True
    
    
if __name__ == "__main__":
    admin_service = AdminService()
    admin_service.get_users_conversation()