from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, Callable, Optional
from database.mysql.model import KnowledgeBasesList,ConversationsList
# 数据库设置
DATABASE_URL = "mysql+pymysql://llmqa_user:www123...@10.116.123.148:3308/llmqa"
# DATABASE_URL = "postgresql://ally:2024@127.0.0.1/sensing"
# engine = create_engine(DATABASE_URL)
# SessionLocal = 
Base = declarative_base()

class MysqlClient:
    def __init__(self,database_url:str=DATABASE_URL):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine,expire_on_commit=False)
    def GetConversationsList(self)->ConversationsList:
        # if session is None:
        session = self.SessionLocal()
        conversations_list = session.query(ConversationsList).all()
        session.close()

        return conversations_list
    def AddKnowledgeBasesList(self,knowledgeBaseName:str)->KnowledgeBasesList:
        # if session is None:
        session = self.SessionLocal()
        new_knowledge_base = KnowledgeBasesList(knowledgeBaseName=knowledgeBaseName)
        session.add(new_knowledge_base)
        session.commit()
        session.close()
        return new_knowledge_base

if __name__ == "__main__":
    mysql_client = MysqlClient()
    conversations_list = mysql_client.AddKnowledgeBasesList("Test")
    print(conversations_list.id)