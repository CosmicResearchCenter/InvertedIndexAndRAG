from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, Text,TIMESTAMP,Boolean
import uuid
from .mysql_client import Base

def generate_id(length=18):
    # 生成一个 UUID
    id_str = str(uuid.uuid4())
    # 将 UUID 前加上 'kb'
    full_id = f'kb{id_str}'
    # 截取指定长度
    return full_id[:length].replace('-', '')

def generate_general_id(length=18):
    # 生成一个 UUID
    id_str = str(uuid.uuid4())
    # 将 UUID 前加上 'kb'
    full_id = f'uu{id_str}'
    # 截取指定长度
    return full_id[:length].replace('-', '')

class KnowledgeBase(Base):
    __tablename__ = 'knowledgeBasesList'
    id = Column(String(18), primary_key=True, default=lambda: str(generate_id(length=18)))
    knowledgeBaseName 	= Column(String(255))

# 对话列表
class Conversation(Base):
    __tablename__ = 'conversationsList'
    id = Column(String(18), primary_key=True, default=lambda: str(generate_general_id(length=18)))
    lastChatTime 	= Column(TIMESTAMP, nullable=False)
    conversationName 	= Column(String(255))
    num_conversation = Column(Integer)
    knowledgeBaseId = Column(String(255))
    userId = Column(String(255))

    def to_dict(self):
        return {
            "conversation_id": self.id,
            "lastChatTime": self.lastChatTime,
            "conversationName": self.conversationName,
            "num_conversation": self.num_conversation,
            "knowledgeBaseId": self.knowledgeBaseId,
            "userId": self.userId
        }
class Chat_Messages (Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True)
    conversationID = Column(String(255))
    timeStamp = Column(TIMESTAMP)
    query = Column(String(255))
    answer = Column(Text)
    userId = Column(String(255)) # 存储用户 ID
    knowledgeBaseId = Column(String(255)) # 存储知识库 ID

class RetrieverDoc(Base):
    __tablename__ = 'retrieverDocs'
    id = Column(String(255), primary_key=True, default=lambda: str(generate_general_id(length=18)))
    content = Column(Text)
    knowledge_doc_name = Column(String(255))
    knowledgeBaseId = Column(String(255))
    messageId = Column(String(255))

# 文档信息
class DocInfo(Base):
    __tablename__ = 'docsInfo'
    id = Column(String(255), primary_key=True, default=lambda: str(generate_general_id(length=18)))
    doc_name = Column(String(255))
    knowledgeBaseId = Column(String(255))
    create_time = Column(TIMESTAMP)
    doc_type = Column(String(255))
    doc_size = Column(Integer)
    save_id = Column(String(255))

class DocIndexStatus(Base):
    __tablename__ = 'docIndexStatus'
    id = Column(String(255), primary_key=True, default=lambda: str(generate_general_id(length=18)))
    index_status = Column(Integer)
    knowledgeBaseId = Column(String(255))
    doc_id = Column(String(255))

    def to_dict(self):
        return {
            "index_status": self.index_status,
            "knowledgeBaseId": self.knowledgeBaseId,
            "doc_id": self.doc_id
        }