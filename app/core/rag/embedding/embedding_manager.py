from embedding.doubao_embedding import DouBaoEmbedding
from embedding.openai_embedding import OpenAIEmbedding
from enum import Enum
from embedding.embedding import Embedding

class EmbeddingType(Enum):
    doubao = "doubao"
    openai = "openai"

    @classmethod
    def get_embedding(cls, name: str):
        for member_name, member in cls.__members__.items():
            if member_name == name:
                return member
        else:
            raise Exception("Not supported embedding type")

class EmbeddingManager:
    def create_embedding(self, name: str = "doubao")->Embedding:
        embedding_type = EmbeddingType.get_embedding(name)
        if embedding_type == EmbeddingType.doubao:
            return DouBaoEmbedding()
        elif embedding_type == EmbeddingType.openai:
            return OpenAIEmbedding()
        else:
            raise Exception("Not supported embedding type")