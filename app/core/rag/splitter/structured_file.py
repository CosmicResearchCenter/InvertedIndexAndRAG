from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from app.core.llm import LLM_Manager,LLM,DouBaoLLM,OpenAILLM
from config.config import LLM_MODEL
class TextSplitter:
    def __init__(self,chunk_size:int=100,chunk_overlap:int=20,length_function:int=len,is_separator_regex:bool=False,split_model:str="OPENAI"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
        self.is_separator_regex = is_separator_regex
        self.split_model = split_model
        self.llm_client = LLM_Manager().creatLLM(split_model)
    # 拆分文本
    def _split_texts(self, text)->List[Document]:
        texst = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self.length_function,
            is_separator_regex=self.is_separator_regex,
        )
        texts = texst.create_documents([text])

        return texts
    def split_texts(self, state_of_the_union:str) -> List[Document]:
        
        return self._split_texts(state_of_the_union)
    
    ###############大模型拆分文本###############
    
    def _SplitText(self,texts:str,splitter_str:str)->List[Document]:
        result:List[Document] = []
        splitted_texts = texts.split(splitter_str)
        for text in splitted_texts:
            result.append(Document(page_content=text))
        return result

    def SplitTextByLLM(self,text:str,splitter_str:str) -> List[Document]:
        # print(len(text))
        
        if len(text)<2000:
            prompt:str = f"""
            请将以下文本拆分成逻辑清晰、内容独立的段落或部分。每个段落应完整表达一个主要思想或主题，并控制段落的长度，使其便于后续的分析和处理。每个段落之间使用指定的拆分符进行分隔，确保拆分后的内容不被修改

            拆分符: {splitter_str}

            请根据文本的结构、主题和意义进行合理拆分：
            {text}
            """
            self.llm_client.setPrompt(prompt="你是一名专业的文本拆分助手，你的任务是帮助用户拆分文本内容。")
            texts = self.llm_client.ChatToBot(content=prompt)
            result = self._SplitText(texts,splitter_str)
            
            return result
        else:
            # 把text分成多个部分，滑动窗口滑动，然后拆分，确保不丢失过多信息
            window_size = 2000  # 滑动窗口的大小
            step_size = 1600    # 滑动步长
            index = 1
            result:List[Document] = []
            for i in range(0, len(text) - window_size + 1, step_size):
                prompt:str = f"""
                请将以下文本拆分成逻辑清晰、内容独立的段落或部分。每个段落应完整表达一个主要思想或主题，并控制段落的长度，使其便于后续的分析和处理。每个段落之间使用指定的拆分符进行分隔，确保拆分后的内容不被修改

                拆分符: {splitter_str}

                请根据文本的结构、主题和意义进行合理拆分：
                {text[i:i + window_size]}
                """               
                self.llm_client.setPrompt(prompt="你是一名专业的文本拆分助手，你的任务是帮助用户拆分文本内容。")
                texts = self.llm_client.ChatToBot(content=prompt)
                item = self._SplitText(texts,splitter_str)
                result.extend(item)
                # result.extend(self._SplitText(texts,splitter_str))
                # print(item)
                # for i in item:
                #     print(i.page_content)
                #     print("---------------------\n")
                print(f"已处理第{index}个块")
                index += 1
            return result

    
if __name__ == "__main__":
    # text = "This is a test. This is another test."
    splitter = TextSplitter()
    docs = splitter.SplitTextByLLM("/Users/markyangkp/Desktop/Projects/llmqa/ocr/tmp_files/data.txt","&&&&&")
    for i in docs:
        print(i.page_content)
        print("---------------------\n\n")