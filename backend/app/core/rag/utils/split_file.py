from ..splitter import PDFSplitter,TextSplitter
from langchain_core.documents import Document
from typing import List
from app.core.ocr.ocr_model import OCR_Model
from config.splitter_model import SplitterModel
from config.config import SPPLITTER_MODEL
def split_file(file_path:str,SPPLITTER_MODEL:SplitterModel=SPPLITTER_MODEL)->List[Document]:
    docs:List[Document] = []
    # 判断文件类型
    if file_path.lower().endswith(".txt"):
        print("txt file")
        with open(file_path) as f:
            state_of_the_union = f.read()
        textSplitter = TextSplitter(SPPLITTER_MODEL)
        docs = textSplitter.split(state_of_the_union)
        return docs
    elif file_path.lower().endswith(".pdf"):
        print("pdf file")
        # pdf文件
        loader = PDFSplitter(file_path=file_path,SPPLITTER_MODEL=SPPLITTER_MODEL)
        docs = loader.split()
        print(docs)
    elif file_path.lower().endswith(".doc"):
        pass
    elif file_path.lower().endswith(".docx"):
        pass
    elif file_path.lower().endswith(".xls"):
        pass
    elif file_path.lower().endswith(".xlsx"):
        pass
    elif file_path.lower().endswith(".ppt"):
        pass
    elif file_path.lower().endswith(".pptx"):
        pass
    elif file_path.lower().endswith(".png"):
        ocr_model = OCR_Model()        
        state_of_the_union = ocr_model.ocr_image_by_file(file_path) 
        textSplitter = TextSplitter(SPPLITTER_MODEL)
        docs = textSplitter.split(state_of_the_union)
    elif file_path.lower().endswith(".jpg"):
        ocr_model = OCR_Model()        
        state_of_the_union = ocr_model.ocr_image_by_file(file_path) 
        textSplitter = TextSplitter(SPPLITTER_MODEL)
        docs = textSplitter.split(state_of_the_union)
    elif file_path.lower().endswith(".jpeg"):
        ocr_model = OCR_Model()        
        state_of_the_union = ocr_model.ocr_image_by_file(file_path) 
        textSplitter = TextSplitter(SPPLITTER_MODEL)
        docs = textSplitter.split(state_of_the_union)
    elif file_path.lower().endswith(".png"):
        ocr_model = OCR_Model()        
        state_of_the_union = ocr_model.ocr_image_by_file(file_path) 
        textSplitter = TextSplitter(SPPLITTER_MODEL)
        docs = textSplitter.split(state_of_the_union)
    elif file_path.lower().endswith(".md"):
        pass
    else:
        raise Exception("File type not support")

    return docs

if __name__ == "__main__":
    file_path = "/Users/markyangkp/Desktop/Projects/llmqa/ocr/testimg.png"
    docs:List[Document] = split_file(file_path,SplitterModel.LLMSplitter)
    print(docs)