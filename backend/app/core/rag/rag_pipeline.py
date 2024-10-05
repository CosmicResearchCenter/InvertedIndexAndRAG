from typing import List,Optional
from app.core.rag.database import ElasticClient,MysqlClient,MilvusCollectionManager
from app.core.rag.embedding import EmbeddingManager,OpenAIEmbedding,DouBaoEmbedding,Embedding
from config.config import EMBEDDING_MODEL_PROVIDER,SPPLITTER_MODEL,LLM_MODEL
# from config.splitter_model import SplitterModel
from .utils.split_file import split_file
from .models.source_document import SourceDocument,SourceDocumentReRanked
from app.core.llm import LLM,LLM_Manager,RerankModel
from app.core.rag.models.document import Document
from app.core.rag.database.mysql.model import KnowledgeBase
from .rerank.rerank import RerankRunner
import os

from .models.knolwedge_base import ResultByDoc

class RAG_Pipeline:
    def __init__(self):
        self.mysql_client = MysqlClient()
        self.es_client = ElasticClient()
        self.milvus_client = MilvusCollectionManager()
        pass
    #创建知识库
    def create_knowledgebase(self, knowledge_base_name: str):
        knowledge_base_id = self.mysql_client.AddKnowledgeBasesList(knowledge_base_name).id
        indexName = self.es_client.create_index(knowledge_base_id)
        self.milvus_client.create_collection(knowledgeBaseID=knowledge_base_id, knowledgeBaseName=knowledge_base_name, dim=1536)
        return knowledge_base_id
    #修改知识库名字
    def modify_knowledgebase(self, new_knowledge_base_name: str,knowledge_base_id: str):
        pass
    #删除知识库
    def delete_knowledgebase(self, knowledge_base_name: str):
        pass
    def show_knowledgebase_list(self):
        knowledgebaseList:List[KnowledgeBase] =  self.mysql_client.GetKnowledgeBasesList()
        return knowledgebaseList
    #文档插入知识库
    def insert_knowledgebase(self,file_path:str, knowledge_base_id: str):
        ### 拆分文档
        docs = split_file(file_path,SPPLITTER_MODEL=SPPLITTER_MODEL)
        ### 插入数据库
        # print("插入数据库")
        #### 写入向量数据库
        # print("写入向量数据库")
        emb_model = EmbeddingManager().create_embedding(EMBEDDING_MODEL_PROVIDER)
        mdata = []
        knowledge_doc_name = os.path.basename(file_path)
        for doc in docs:
            content = doc.page_content
            vector = emb_model.embed_with_str(content, "document")
            item = {
                "content": content,
                "knowledge_doc_name": knowledge_doc_name,
                "vector": vector
            }
            mdata.append(item)
        
        self.milvus_client.insert_data(mdata, knowledge_base_id)
        # milvus_client.create_index(nlist=128)
        ### 写入 ElasticSearch
        # print("写入 ElasticSearch")
        success,failed = self.es_client.insert_data(docs,knowledge_base_id,knowledge_doc_name)
        print(f"成功插入 {success} 条数据，失败 {len(failed)} 条数据")
        # return success,failed
    #文档召回
    def retriever_by_knowledgebase(self,question:str, knowledge_base_id: str):
        
        embeddingMode = EmbeddingManager().create_embedding(EMBEDDING_MODEL_PROVIDER)
        vecotr = embeddingMode.embed_with_str(question,"query")
        
        result:List[SourceDocument] = []
        
        result_milvus = self.milvus_client.search(vecotr,knowledge_base_id)
        i = 0
        for item in result_milvus[0]:
            content = item.entity.content
            knowledge_doc_name = item.entity.knowledge_doc_name
            sourceDoc = SourceDocument(content=content,knowledge_doc_name=knowledge_doc_name)
            result.append(sourceDoc)
            i += 1
            if i == 5:
                break
        
        result_elastic = self.es_client.search(question,knowledge_base_id)
        
        i = 0
        for item in result_elastic:
            content = item["_source"]["content"]
            knowledge_doc_name = item["_source"]["knowledgeDocName"]
            sourceDoc = SourceDocument(content=content,knowledge_doc_name=knowledge_doc_name)
            result.append(sourceDoc)
            i += 1
            if i == 5:
                break
        return result
    
    # ReRank评估
    def re_rank(self,question:str,documents: list[Document], score_threshold: Optional[float] = None,
            top_n: Optional[int] = None):
        rerank_model = RerankModel()
        rerank_runner = RerankRunner(rerank_model)
        rerank_result = rerank_runner.run(question, documents, score_threshold=score_threshold, top_n=top_n)

        return rerank_result
    
    #生成回答
    def generate_answer_by_knowledgebase(self, question:str,knowledge_base_id:str,history_messages=[])->ResultByDoc:
        print("generate_answer_by_knowledgebase")
        print(history_messages)
        # 获取文档源信息
        source_docs:List[SourceDocument] = self.retriever_by_knowledgebase(question,knowledge_base_id)

        documents:List[Document] = []
        for source in source_docs:
            # print(source.content+"\n#####")
            documents.append(Document(
                                    page_content=source.content,
                                    metadata={
                                        "knowledge_doc_name": source.knowledge_doc_name
                                    })
                            )
        # ReRank评估
        rerank_result = self.re_rank(question=question,documents=documents,score_threshold=0.01,top_n=4)

        prompt_source = ""
        source_docs_reranked:List[SourceDocumentReRanked] = []

        for result in rerank_result:
            prompt_source += f"""
            {result.page_content}\n
            """
            source_docs_reranked.append(SourceDocumentReRanked(
                                content=result.page_content,
                                knowledge_doc_name=result.metadata['knowledge_doc_name'],
                                socre=result.metadata['score']
                            ))
            # print(result.metadata['score'])
        
        # for result in source_docs:
        #     prompt_source += f"""
        #     {result.content}\n
        #     """
        #     source_docs_reranked.append(SourceDocumentReRanked(
        #                         content=result.content,
        #                         knowledge_doc_name=result.knowledge_doc_name,
        #                         socre=0.00
        #                     ))
        #     # print(result.metadata['score'])

        print(prompt_source)
        llm = LLM_Manager().creatLLM(mode_provider="OPENAI")
        prompt_system =f"""
        你是一个基于文档提供高质量回答的助手。你的任务是根据提供的文档内容，准确、清晰地回答用户的问题。请确保以下几点：

        1. 基于文档：你的回答应严格基于提供的文档内容，避免编造信息。如果文档中没有相关信息，请明确告知用户。
        2. 准确性：回答应尽可能准确，避免模糊或不确定的表达。如果某些部分是合理推测，请明确说明。
        3. 简洁明了：尽量简洁明了地表达你的回答，不使用多余的细节。
        4. 专业性：回答应保持专业性和客观性，避免使用主观或情感化的语言。

        你将收到召回的文档内容以及用户的问题，请在此基础上生成回答。
        """ 
        prompt = f"""
        你是一个基于文档提供高质量回答的助手。你的任务是根据提供的文档内容，准确、清晰地回答用户的问题。
        现在请你完成以下任务：
        请根据用户问题，使用召回的知识库中的信息进行推理回答。请确保回答内容准确。
        要求：
        1. 使用文档中的信息来推理回答问题，并确保答案准确。
        2. 如果文档中没有明确的信息，可以合理推断，但要标注推断部分。
        3. 尽量简洁明了地表达。
        ######################################\n
        用户问题:
        {question}
        ######################################\n
        知识库内容:
        {prompt_source}
        """
        llm.addHistory(history_messages)
        llm.setPrompt(prompt_system)
        answer = llm.ChatToBot(prompt)
        # print(answer)
        return ResultByDoc(answer=answer,source=source_docs_reranked,query=question)
if __name__ == "__main__":
    # 创建知识库
    pipelines = RAG_Pipeline()
    # kb4cc1c0b5d7164a
    # knowledge_base_id = pipelines.create_knowledgebase(knowledge_base_name="第二个测试")
    # print(knowledge_base_id)    
    # 插入文档
    pipelines.insert_knowledgebase("/Users/markyangkp/Desktop/Projects/llmqa/ocr/tmp_files/data.txt", "kb1bba5c96d9414c")
    # 生成回答
    # question = "荣耀理发店的营业时间是多少？"
    # answer = pipelines.generate_answer_by_knowledgebase(question,"kbf11defac6e0043")
    # print(answer)