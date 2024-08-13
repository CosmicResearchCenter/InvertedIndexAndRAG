from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType,IndexType
from pymilvus import SearchResult,Hits,Hit
import numpy as np
from config.config import MILVUS_PORT, MILVUS_HOST
class MilvusCollectionManager:
    def __init__(self, host: str = MILVUS_HOST, port: int = MILVUS_PORT):
        self.host = host
        self.port = port
        self.collection = None
        self.connect()

    def connect(self):
        """连接到Milvus服务器"""
        connections.connect("default", host=self.host, port=self.port)
        print(f"Connected to Milvus at {self.host}:{self.port}")

    def create_collection(self, knowledgeBaseID: str,knowledgeBaseName:str, dim: int):
        """创建集合"""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="knowledge_doc_name", dtype=DataType.VARCHAR, max_length=512)
        ]
        schema = CollectionSchema(fields, description=knowledgeBaseName)
        self.collection = Collection(name=knowledgeBaseID, schema=schema)
        print(f"Collection '{knowledgeBaseID}' created with dimension {dim}")

    def load_collection(self, knowledgeBaseID: str):
        """加载现有集合"""
        self.collection = Collection(name=knowledgeBaseID)
        print(f"Collection '{knowledgeBaseID}' loaded")

    def insert_data(self, data,knowledgeBaseID):
        self.load_collection(knowledgeBaseID)
        """插入数据到集合"""
        if self.collection is None:
            raise ValueError("No collection is loaded or created")

        # ids = list(range(self.collection.num_entities, self.collection.num_entities + len(data)))
        vectors = [item["vector"] for item in data]
        contents = [item["content"] for item in data]
        knowledge_doc_names = [item["knowledge_doc_name"] for item in data]  # 新增字段

        entities = [
            # ids,  # ID字段
            vectors,  # 向量字段
            contents,  # 内容字段
            knowledge_doc_names  # 新增字段
        ]
        self.collection.insert(entities)
        self.collection.flush()
        print(f"Inserted {len(data)} entities into collection '{self.collection.name}'")

    def create_index(self, index_type: str = "IVF_FLAT", nlist: int = 128):
        """为向量字段创建索引"""
        if self.collection is None:
            raise ValueError("No collection is loaded or created")
        
        index_params = {
            "index_type": index_type,
            "params": {"nlist": nlist}
        }
        self.collection.create_index(field_name="vector", index_params=index_params)
        print(f"Index created for collection '{self.collection.name}' with type '{index_type}'")

    def search(self, query_vector,collection:str, limit: int = 10, nprobe: int = 256,)->SearchResult:
        self.load_collection(collection)
        """在集合中搜索相似向量"""
        if self.collection is None:
            raise ValueError("No collection is loaded or created")

        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": nprobe}
        }
        results = self.collection.search([query_vector], "vector", search_params, limit=limit,output_fields=["content","knowledge_doc_name"])
        return results

    def get_content_by_id(self, entity_id):
        """根据ID获取内容"""
        if self.collection is None:
            raise ValueError("No collection is loaded or created")

        content = self.collection.query(expr=f"id == {entity_id}", output_fields=["content"])
        if content:
            return content[0]["content"]
        else:
            return None

# 使用示例
if __name__ == "__main__":
    manager = MilvusCollectionManager()

    # 创建新的集合
    manager.create_collection(knowledgeBaseID="kb292f83a3955549",knowledgeBaseName="Test", dim=2048)

    # # 或加载现有集合
    # # manager.load_collection(name="document_segments")

    # # 插入数据
    # data = [
    #     {"content": "This is a new paragraph.", "vector": np.random.random(128).tolist()},
    #     {"content": "Another new paragraph.", "vector": np.random.random(128).tolist()},
    #     # 更多数据
    # ]
    # manager.insert_data(data)

    # # 创建索引
    # manager.create_index()

    # # 搜索示例
    # query_vector = np.random.random(128).tolist()
    # results = manager.search(query_vector)
    # for result in results[0]:
    #     print(f"ID: {result.id}, Distance: {result.distance}")
    #     content = manager.get_content_by_id(result.id)
    #     print(f"Content: {content}")
