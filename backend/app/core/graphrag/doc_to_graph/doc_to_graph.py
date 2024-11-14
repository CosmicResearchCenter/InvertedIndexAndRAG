from ..prompt_template.prompt_template import PromptTemplate
from ..prompt_template.prompts import entity_relation_prompt,entity_abstract_prompt,entity_extraction_prompt
from app.core.llm.llm_manager import LLM_Manager
from config.config_info import settings
import json
class DocToGraph:
    def __init__(self) -> None:
        self.entity_lable_list = []
        # self.entity_abstract_list = []
        self.entity_list = []
        self.entity_relation_list = []
        pass
    # 读取文档
    def read_doc(self,doc_path:str) -> str:
        with open(doc_path, 'r') as f:
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
        
    
    # 提取文档中的抽象实体
    def entity_abstract(self, text: str) -> str:
        prompt = PromptTemplate(
                        template=entity_abstract_prompt,
                        input_variables=['entity_lable_list','text']            
                    )
        llm = LLM_Manager().creatLLM(settings.LLM_PROVIDER)
        entity_lable_list_str = ",".join(self.entity_lable_list)
        prompt = prompt.render(
            entity_lable_list = entity_lable_list_str,
            text = text
        )
        answer:str = llm.ChatToBot(prompt)
        
        answer.replace(" ","") 
        entity_lable_list = answer.split(",")
        self.entity_lable_list.extend(entity_lable_list)
    
    # 提取文档中的实体
    def entity_extraction(self, text: str) -> str:
        prompt = PromptTemplate(
                        template=entity_extraction_prompt,
                        input_variables=['entity_list', 'text']
                    )
        llm = LLM_Manager().creatLLM(settings.LLM_PROVIDER)
        
        entity_lable_list_str = ",".join(self.entity_lable_list) 
        answer: str = prompt.render(
            entity_list=str(self.entity_list),
            entity_lable_list=entity_lable_list_str,
            text=text
        )
        
        answer = llm.ChatToBot(answer)
        
        # 解析文本 文本转json
        json_data = self.text_to_json(answer) 
        
        print(json_data)
        
        self.entity_list.extend(json_data)
        
        
    
    # 建立文档中实体对象之间的关系
    def entity_relation(self, text: str) -> str:
        prompt = PromptTemplate(
                        template=entity_relation_prompt,
                        input_variables=['entity_relation_list', 'text', 'entity_list']
                    )
        llm = LLM_Manager().creatLLM(settings.LLM_PROVIDER)
        
        prompt = prompt.render(
            entity_relation_list=str(self.entity_relation_list),
            text=text,
            entity_list=str(self.entity_list)
        )
        
        answer: str = llm.ChatToBot(prompt)

        # 解析文本 文本转json
        json_data = self.text_to_json(answer)
        
        if json_data:
            self.entity_relation_list.extend(json_data)
            print(json_data)
        
if __name__ == "__main__":
    doc_to_graph = DocToGraph()
    text = doc_to_graph.read_doc('/Users/markyangkp/Desktop/Projects/InvertedIndexAndRAGAI/docs/graphrag_test_txt.txt')
    doc_to_graph.entity_abstract(text)
    doc_to_graph.entity_extraction(text)
    doc_to_graph.entity_relation(text)