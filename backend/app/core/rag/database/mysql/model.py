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
class KnowledgeBasesList(Base):
    __tablename__ = 'knowledgeBasesList'
    id = Column(String, primary_key=True, default=lambda: str(generate_id()))
    knowledgeBaseName 	= Column(String)
    
class ConversationsList(Base):
    __tablename__ = 'conversationsList'
    id = Column(String, primary_key=True, default=lambda: str(generate_id()))
    lastChatTime 	= Column(TIMESTAMP)
    conversationName 	= Column(String)
    num_conversation = Column(Integer)
    dataSourceName = Column(String)
    dataSourceID = Column(String)
