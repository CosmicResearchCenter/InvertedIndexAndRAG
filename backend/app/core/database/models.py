from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, Text,TIMESTAMP
import uuid

Base = declarative_base()

def generate_id(length=18):
    # 生成一个 UUID
    id_str = str(uuid.uuid4())
    # 将 UUID 前加上 'kb'
    full_id = f'kb{id_str}'
    # 截取指定长度
    return full_id[:length].replace('-', '')

class KnowledgeBase(Base):
    __tablename__ = 'knowledgeBasesList'
    id = Column(String, primary_key=True, default=lambda: str(generate_id()))
    knowledgeBaseName 	= Column(String)

# 对话列表
class Conversation(Base):
    __tablename__ = 'conversationsList'
    id = Column(String, primary_key=True, default=lambda: str(generate_id()))
    lastChatTime 	= Column(TIMESTAMP, nullable=False)
    conversationName 	= Column(String)
    num_conversation = Column(Integer)
    knowledgeBaseId = Column(String)
    userId = Column(String)

class Chat_Messages (Base):
    __tablename__ = 'chat_messages'
    id = Column(String, primary_key=True, default=lambda: str(generate_id()))
    conversationID = Column(String)
    timeStamp = Column(TIMESTAMP)
    query = Column(String)
    answer = Column(String)
    userId = Column(String) # 存储用户 ID
    knowledgeBaseId = Column(String) # 存储知识库 ID
    retrieverDocId = Column(String) # 存储检索文档的 ID

class RetrieverDoc(Base):
    __tablename__ = 'retrieverDocs'
    id = Column(String, primary_key=True, default=lambda: str(generate_id()))
    title = Column(Text)
    content = Column(Text)
    source = Column(String)
    url = Column(String)
    knowledgeBaseId = Column(String)
    messageId = Column(String)
