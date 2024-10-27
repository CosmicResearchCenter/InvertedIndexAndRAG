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
        conversation = self.mysql_session.query(Conversation).filter(Conversation.id==conversation_id , Conversation.delete_sign == False).first()
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
            print(f"knowledgeBaseId:{conversation.knowledgeBaseId}")
            knowledgebase = self.mysql_session.query(KnowledgeBase).filter(KnowledgeBase.id==conversation.knowledgeBaseId , KnowledgeBase.delete_sign==False).first()
            if knowledgebase is None:
                raise ValueError("Knowledge base not found")
            else:
                return knowledgebase
            
        except Exception as e:
            print(f"Erreor:{e}")

    # 更改知识库
    def change_knowledgebase(self, conversation_id,knowledgeBaseId,user_id):
        try:
            conversation = self.match_conversations(conversation_id,user_id)
            conversation.knowledgeBaseId = knowledgeBaseId
            self.mysql_session.commit()
            self.mysql_session.refresh(conversation)
            return conversation
        except Exception as e:
            print(e)
    # 删除对话
    def delete_conversation(self, conversation_id):
        try:
            conversation = self.mysql_session.query(Conversation).filter(Conversation.id==conversation_id , Conversation.delete_sign == False , Conversation.userId == self.user_id).first()
            if conversation is None:
                raise ValueError("Conversation not found")
            else:
                conversation.delete_sign = True
                self.mysql_session.commit()
                self.mysql_session.refresh(conversation)
                return conversation
            
        except Exception as e:
            print(e)
    # 重命名对话
    def rename_conversation(self, conversation_id, new_name):
        try:
            conversation = self.mysql_session.query(Conversation).filter(Conversation.id==conversation_id , Conversation.delete_sign == False , Conversation.userId == self.user_id).first()
            if conversation is None:
                raise ValueError("Conversation not found")
            else:
                conversation.conversationName = new_name
                self.mysql_session.commit()
                self.mysql_session.refresh(conversation)


                return conversation
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
                    current_knowledge_baseid=message.knowledgeBaseId,
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
    def answer_question(self, resultByDoc: ResultByDoc,history_message=[],streaming=False):
        rAG_Pipeline = RAG_Pipeline()
            
        answer = rAG_Pipeline.generate_answer_by_knowledgebase(resultByDoc=resultByDoc,history_messages=history_message,streaming=streaming)
        if isinstance(answer, str):
            print("Answer:", answer)
            return answer
        else:
            for item in answer:
                yield item


    # 获取对话列表
    def get_conversation_list(self,user_id):
        conversations = self.mysql_session.query(Conversation).filter(Conversation.delete_sign == False , Conversation.userId == user_id ).all()
        return conversations
    # 先获取召唤文档
    def get_retrieve_documents(self, question,knowledgebase_id)->ResultByDoc:
        rAG_Pipeline = RAG_Pipeline()
        try:
            resultByDoc:ResultByDoc = rAG_Pipeline.retrieve_documents(question=question,knowledge_base_id=knowledgebase_id)
            return resultByDoc
        except Exception as e:
            print(e)
    # 处理用户输入
    def run(self, chatMessageRequest: ChatMessageRequest, streaming=False):
        # 获取用户输入
        convseration_id = chatMessageRequest.conversation_id
        user_id = chatMessageRequest.user_id
        message = chatMessageRequest.message
        # streaming = chatMessageRequest.streaming
        # 匹配对话
        try:
            conversation: Conversation = self.match_conversations(convseration_id, user_id)
            knowledgebase = self.match_knowledgebase(convseration_id, user_id)

            # 加载对话记录
            messages = self.load_conversation(conversation.id)
            messageLog = self.format_conversation_Log(messages)

            # 获取检索文档
            resultByDoc: ResultByDoc = self.get_retrieve_documents(question=message, knowledgebase_id=knowledgebase.id)

            # 保存对话记录
            new_message = Chat_Messages(
                conversationID=conversation.id,
                query=message,
                answer="",
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

            answer = ""
            # 生成回答
            if streaming:
                answer_generator  = self.answer_question(resultByDoc=resultByDoc,  history_message=messageLog, streaming=True)
                if isinstance(answer_generator, str):
                    pass
                else:
                    
                    for item in answer_generator :
                        yield item
                        answer+=item
                    # 流式输出完成后更新答案到数据库
                    new_message.answer = answer
                    self.mysql_session.commit()  # 更新数据库
                    self.mysql_session.refresh(new_message)
            else:
                answer = self.answer_question(resultByDoc=resultByDoc,  history_message=messageLog, streaming=False)
                if isinstance(answer, str):
                    
                    new_message.answer = answer
                    self.mysql_session.commit()  # 更新数据库
                    self.mysql_session.refresh(new_message)
                    return answer
                else:
                    for item in answer:
                        yield item

        except Exception as e:
            print(f"Error: {e}")

    




"""
临时梳理逻辑

前端先选择知识库，如果没有知识库则返回错误

然后再发起对会

后端对于空的对话id和选择的知识库id 还有userid，创建对话
并根据知识库回答问题

如果是已有的对话，则匹配对话，并根据知识库回答问题


所以需要有一个创建对话的接口，不能根据判断对话id是否为空来创建对话

"""