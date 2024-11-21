from ..prompt_template.prompt_template import PromptTemplate
from ..prompt_template.entity_types import ENTITY_TYPE_GENERATION_JSON_PROMPT
from ..prompt_template.entity_extraction import GRAPH_EXTRACTION_JSON_PROMPT
from ..prompt_template.extraction import GRAPH_EXTRACTION_PROMPT
from ..prompt_template.entity_relationship import ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT
from app.core.llm.llm_manager import LLM_Manager
from config.config_info import settings
import json
from ..graph_to_base.neo4j_client import Neo4jClient
class DocToGraph:
    def __init__(self) -> None:
        self.entity_types = None
        self.entity_list = []
        self.entity_relation_list = []
    
    def read_doc(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text
    def text_to_json(self,text:str):
        # 去除可能存在的Markdown代码块标记
        text = text.strip().strip('```json').strip('```')
        
        try:
            # 尝试将文本解析为JSON对象
            json_obj = json.loads(text)
            
            return json_obj
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None

    def entity_types_extraction(self,task:str ,text: str):
        prompt = PromptTemplate(
                        template=ENTITY_TYPE_GENERATION_JSON_PROMPT,
                        input_variables=['task', 'input_text']
                    )
        llm = LLM_Manager().creatLLM(settings.LLM_PROVIDER)
        
        query: str = prompt.render(
            task=task,
            input_text = text
        )
        # print(query)
        answer = llm.ChatToBot(query)
        # print(answer)
        self.entity_types = self.text_to_json(answer)
    def entity_extraction(self, text: str):
        prompt = PromptTemplate(
                        template=GRAPH_EXTRACTION_PROMPT,
                        input_variables=['entity_types', 'tuple_delimiter','completion_delimiter','record_delimiter','input_text']
                    )
        llm = LLM_Manager().creatLLM(settings.LLM_PROVIDER)
        # {"entity_types": ["person", "organization", "political party", "government position", "event", "policy", "publication", "relationship"] }
        entity_types = ""
        for i in self.entity_types['entity_types']:
            entity_types += i + ','

        query: str = prompt.render(
            entity_types=entity_types,
            tuple_delimiter = ',',
            completion_delimiter = '\n\n',
            record_delimiter = '\n',
            input_text = text
        )
        # print(query)
        answer = llm.ChatToBot(query)
        print(answer)
    def entity_relationship_extraction(self, text: str):
        prompt = PromptTemplate(
                        template=ENTITY_RELATIONSHIPS_GENERATION_JSON_PROMPT,
                        input_variables=['entity_types', 'text']
                    )
        llm = LLM_Manager().creatLLM(settings.LLM_PROVIDER)
        # {"entity_types": ["person", "organization", "political party", "government position", "event", "policy", "publication", "relationship"] }
        entity_types = ""
        for i in self.entity_types['entity_types']:
            entity_types += i + ','

        query: str = prompt.render(
            entity_types=entity_types,
            input_text = text
        )
        # print(query)
        answer = llm.ChatToBot(query)
        # print(answer)
        entity_relation_list = self.text_to_json(answer)
        self.entity_relation_list.extend(entity_relation_list)
        
if __name__ == "__main__":
    doc_to_graph = DocToGraph()
    # neo4j_client = Neo4jClient(uri="bolt://222.199.255.41:7687", username="neo4j", password="www123...")
    text = doc_to_graph.read_doc('E:/Projects/InvertedIndexAndRAG/docs/trump.txt')
    task = input("这个文档的主要用途:")
    doc_to_graph.entity_types_extraction(task,text)
    print(doc_to_graph.entity_types)
    # doc_to_graph.entity_relationship_extraction(text)
    # print(doc_to_graph.entity_relation_list)
    doc_to_graph.entity_extraction(text)
    # print(doc_to_graph.entity_label_list)
    # doc_to_graph.entity_extraction(text)
    # for entity in doc_to_graph.entity_list:
    #     print(entity)
    #     neo4j_client.create_entity(entity)
    # doc_to_graph.entity_relation(text)
    # for entity_relation in doc_to_graph.entity_relation_list:
    #     print(entity_relation)
    #     neo4j_client.create_entity_relation(entity_relation)
    # neo4j_client.close()