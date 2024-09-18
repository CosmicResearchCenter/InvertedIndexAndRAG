from abc import ABC, abstractmethod
class Embedding(ABC):
    @abstractmethod
    def embed_with_str(self, text: str) -> list[float]:
        pass
