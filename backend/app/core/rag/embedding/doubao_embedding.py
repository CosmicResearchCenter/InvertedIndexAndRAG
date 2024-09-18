import numpy as np
from volcenginesdkarkruntime import Ark
from .embedding import Embedding
from typing import List
from config.config import DOUBAO_API_KEY
class DouBaoEmbedding(Embedding):
    def __init__(self,api_key:str=DOUBAO_API_KEY):
        self.client = Ark(
            api_key=api_key,
        )
    def embed_with_str(self,text:str,embType:str)-> list[float]:
        if embType == "query":
            query_instruction:str = '为这个句子生成表示以用于检索相关文章:'
            resp = self.client.embeddings.create(
                model="ep-20240703010240-hsbv9",
                input=[query_instruction+text],
                # text_type=type
                )
        elif embType == "document": 
            resp = self.client.embeddings.create(
                model="ep-20240703010240-hsbv9",
                input=[text],
                # text_type=type
                )
        else:
            raise Exception("embType is not valid")
        return resp.data[0].embedding
def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_vector1 = np.linalg.norm(vector1)
    norm_vector2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm_vector1 * norm_vector2)
    return similarity

# print(len(em.embed_with_str("你好","query")))
if __name__ == '__main__':
    em = DouBaoEmbedding()
    
    v1 = em.embed_with_str("00000-01293019",'query')
    v2 = em.embed_with_str("学校各个网站链接北京化工大学官网www.buct.edu.cn教务管理系统jwglxt.buct.edu.cn教务处网站jiaowuchu.buct.edu.cn","document")
    print(len(v1))
    cos = cosine_similarity(v1,v2)

    print("相似度1:"+str(cos))


    v1 = em.embed_with_str("校外人员进校参观的流程是什么？",'query')
    v2 = em.embed_with_str("校外人员进校参观预约流程：1、学生提供预约链接 2、访客填写访客信息 3、等待审批","document")

    cos = cosine_similarity(v1,v2)

    print("相似度2:"+str(cos))