import requests
from .embedding import Embedding
from config.config_info import settings

class SiliconFlowEmbedding(Embedding):
    def __init__(self, 
                 base_url: str = getattr(settings, 'SILICONFLOW_BASE_URL', 'https://api.siliconflow.cn'),
                 api_key: str = getattr(settings, 'SILICONFLOW_API_KEY', ''),
                 model: str = getattr(settings, 'SILICONFLOW_EMBEDDING_MODEL', 'BAAI/bge-large-zh-v1.5')):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def embed_with_str(self, text: str, embType: str) -> list[float]:
        payload = {
            "model": self.model,
            "input": text,
            "encoding_format": "float"
        }
        
        response = requests.post(
            f"{self.base_url}/v1/embeddings", 
            json=payload, 
            headers=self.headers
        )
        
        response_data = response.json()
        return response_data["data"][0]["embedding"]
