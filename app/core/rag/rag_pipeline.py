from typing import List
from .database import ElasticClient,MysqlClient,MilvusCollectionManager
from .embedding import EmbeddingManager,OpenAIEmbedding,DouBaoEmbedding,Embedding
from config.config import EMBEDDING_MODEL_PROVIDER

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
    def insert_knowledgebase(self,file_path:str, knowledge_base_name: str,knowledge_base_id: str):
        ### 拆分文档
        
        ### 插入数据库
        print("插入数据库")
    #文档召回
    def retriever_by_knowledgebase(self,question:str, knowledge_base_id: str):
        """
        从 Elasticsearch 和 Milvus 中获取文档源信息

        Args:
            question (str): 用户输入的查询问题
            doc_name (str): 指定的文档名称

        Returns:
            None: 此函数无返回值，仅执行查询操作

        """
        esClient = ElasticClient()
        milvusClient = MilvusCollectionManager()

        embeddingMode = EmbeddingManager().create_embedding(EMBEDDING_MODEL_PROVIDER)

        vecotr = embeddingMode.embed_with_str(question,"query")

        result_milvus = milvusClient.search(vecotr,knowledge_base_id)

        result_elastic = esClient.search(question,knowledge_base_id)
        
        return result_elastic,result_milvus
        pass
    #生成回答
    def generater_answer_by_knowledgebase(self, knowledge_base_name: str):
        pass