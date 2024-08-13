from typing import List

class RAG_Pipelines:
    def __init__(self):
        pass
    #创建知识库
    def create_knowledgebase(self, knowledge_base_name: str):
        pass
    #修改知识库名字
    def modify_knowledgebase(self, knowledge_base_name: str):
        pass
    #删除知识库
    def delete_knowledgebase(self, knowledge_base_name: str):
        pass
    #文档插入知识库
    def insert_knowledgebase(self, knowledge_base_name: str):
        pass
    #文档召回
    def retriever_by_knowledgebase(self, knowledge_base_name: str):
        pass
    #生成回答
    def generater_answer_by_knowledgebase(self, knowledge_base_name: str):
        pass