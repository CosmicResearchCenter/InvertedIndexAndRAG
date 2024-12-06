from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, Callable, Optional
from .model import KnowledgeBase,ConversationsList
from typing import List
from config.config_info import settings
import datetime,time
user = settings.MYSQL_USER
password = settings.MYSQL_PASSWORD
ip = settings.MYSQL_IP
port = settings.MYSQL_PORT
basename = settings.MYSQL_BASE

# 数据库设置
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{ip}:{port}/{basename}"
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
    # 添加知识库Name和ID到表里
    def AddKnowledgeBasesList(self,knowledgeBaseName:str,userId:str)->KnowledgeBase:
        # if session is None:
        session = self.SessionLocal()
        create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        update_time = create_time
        new_knowledge_base = KnowledgeBase(knowledgeBaseName=knowledgeBaseName,
                                           created_by=userId,
                                           create_time=create_time,
                                           update_time=update_time)
        session.add(new_knowledge_base)
        session.commit()
        session.close()
        return new_knowledge_base
    def GetKnowledgeBasesList(self)->List[KnowledgeBase]:
        # if session is None:
        session = self.SessionLocal()
        knowledge_bases_list = session.query(KnowledgeBase).all()
        session.close()
        return knowledge_bases_list

if __name__ == "__main__":
    mysql_client = MysqlClient()
    conversations_list = mysql_client.GetKnowledgeBasesList()
    print(conversations_list[-1].knowledgeBaseName)