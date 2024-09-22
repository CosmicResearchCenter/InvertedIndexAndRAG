from app.core.llm import LLM,LLM_Manager
from app.core.database.mysql_client import MysqlClient
from app.core.database.models import Conversation,KnowledgeBase,Chat_Messages,RetrieverDoc 
from app.models.chat_models import ChatMessageRequest
from app.core.rag.rag_pipeline import RAG_Pipeline
from app.core.rag.models.knolwedge_base import ResultByDoc
from app.core.chat.chat_type import ChatMessageHistory,RetrieverDoc as RetrieverDocs
import datetime
from typing import List

class Chat:
    def __init__(self, conversation_id,user_id):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.mysql_session = MysqlClient().SessionLocal()
    
    def __del__(self):
        self.mysql_session.close()
    #创建对话
    def create_conversation(self,knowledgeBaseId:str,user_id)->Conversation:
        try:
            new_conversation = Conversation(num_conversation=0,knowledgeBaseId=knowledgeBaseId,userId=user_id,conversationName="New Conversation",lastChatTime=datetime.datetime.now())                 
            self.mysql_session.add(new_conversation)
            self.mysql_session.commit()
            self.mysql_session.refresh(new_conversation)
            # print("Conversation created successfully")
            return new_conversation
        except Exception as e:
            print(e)
    
    
    #匹配对话
    def match_conversations(self, conversation_id,user_id)->Conversation:
        conversation = self.mysql_session.query(Conversation).filter(Conversation.id==conversation_id).first()
        if conversation is None:
            raise ValueError("Conversation not found")
        elif conversation.userId != user_id:
            raise ValueError("Conversation does not belong to the current user")
        else:
            return conversation
        
    # 匹配知识库
    def match_knowledgebase(self, conversation_id,user_id)->KnowledgeBase:
        try:
            conversation = self.match_conversations(conversation_id,user_id)
            print(conversation_id)
            knowledgebase = self.mysql_session.query(KnowledgeBase).filter(KnowledgeBase.id==conversation.knowledgeBaseId).first()
            if knowledgebase is None:
                raise ValueError("Knowledge base not found")
            else:
                return knowledgebase
            
        except Exception as e:
            print(e)
    
    # 加载对话
    def load_conversation(self, conversation_id)->List[ChatMessageHistory]:
        # 查询对话记录
        try:
            messages = self.mysql_session.query(Chat_Messages).filter(Chat_Messages.conversationID == conversation_id).all()

            messages_history:List[ChatMessageHistory] = []

            for message in messages:
                messages_history_item = ChatMessageHistory(
                    conversation_id=message.conversationID,
                    query=message.query,
                    answer=message.answer,
                    retriever_docs=[]
                )
                retriever_docs = self.mysql_session.query(RetrieverDoc).filter(RetrieverDoc.messageId == message.id).all()

                for doc in retriever_docs:
                    retrieverDoc:RetrieverDocs = RetrieverDocs(
                        content=doc.content,
                        knowledge_doc_name=doc.knowledge_doc_name,
                        knowledgeBaseId=doc.knowledgeBaseId,
                    )
                    messages_history_item.retriever_docs.append(retrieverDoc)
                messages_history.append(messages_history_item)



            return messages_history
        except Exception as e:
            print(e)
    
    # 格式化对话记录
    def format_conversation_Log(self, messages:List[Chat_Messages]):
        messageLog = []
        for message in messages:
            formatted_message = {
                "role": "user",
                "content": message.query
            }
            messageLog.append(formatted_message)
            formatted_message = {
                "role": "assistant",
                "content": message.answer
            }
            messageLog.append(formatted_message)
        return messageLog

    # 保存对话
    def save_conversation(self, message:Chat_Messages):
        try:
            self.mysql_session.add(message)
            self.mysql_session.commit()
            self.mysql_session.refresh(message)
        except Exception as e:
            print(e)
    
    # 回答问题
    def answer_question(self, question,knowledgebase_id,history_message=[])->ResultByDoc:
        rAG_Pipeline = RAG_Pipeline()

        resultByDoc:ResultByDoc = rAG_Pipeline.generate_answer_by_knowledgebase(question=question,knowledge_base_id=knowledgebase_id,history_messages=history_message)

        return resultByDoc

    # 生成回复
    def generate_response(self, input_text):
        pass
    # 处理用户输入
    def run(self,chatMessageRequest:ChatMessageRequest):
        # 获取用户输入
        convseration_id = chatMessageRequest.conversation_id
        user_id = chatMessageRequest.user_id
        message = chatMessageRequest.message

        # 匹配对话
        try:
            conversation:Conversation = self.match_conversations(convseration_id,user_id)
            knowledgebase = self.match_knowledgebase(convseration_id,user_id)

            # 加载对话记录
            messages = self.load_conversation(conversation.id)
            messageLog = self.format_conversation_Log(messages)
            try:
                resultByDoc:ResultByDoc = self.answer_question(question=message,knowledgebase_id=knowledgebase.id,history_message=messageLog)
                
                # 保存对话记录
                new_message = Chat_Messages(
                    conversationID=conversation.id,
                    query=message,
                    answer=resultByDoc.answer,
                    userId=user_id,
                    knowledgeBaseId=knowledgebase.id,
                )
                self.save_conversation(new_message)

                # 保存检索文档
                for doc in resultByDoc.source:
                    retriever_doc = RetrieverDoc(
                        content=doc.content,
                        knowledge_doc_name=doc.knowledge_doc_name,
                        knowledgeBaseId=knowledgebase.id,
                        messageId=new_message.id
                    )
                    self.mysql_session.add(retriever_doc)
                    self.mysql_session.commit()
                    


                

            # 返回历史聊天记录、检索文档和答案，聊天记录并附带聊天文档
                return resultByDoc
            except Exception as e:
                print(e)


        except Exception as e:
            print(e)

        pass
    
    




"""
临时梳理逻辑

前端先选择知识库，如果没有知识库则返回错误

然后再发起对会

后端对于空的对话id和选择的知识库id 还有userid，创建对话
并根据知识库回答问题

如果是已有的对话，则匹配对话，并根据知识库回答问题


所以需要有一个创建对话的接口，不能根据判断对话id是否为空来创建对话

"""