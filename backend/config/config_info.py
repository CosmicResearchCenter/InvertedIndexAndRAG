from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    MYSQL_IP:str
    MYSQL_PORT:str
    MYSQL_BASE:str
    MYSQL_USER:str
    MYSQL_PASSWORD:str

    EMBEDDING_MODEL_PROVIDER :str 
    LLM_PROVIDER :str
    # 0 1
    SPPLITTER_MODEL :int

    # ES_BASE_URL
    ES_BASE_URL :str 
    ES_BASE_PORT :int 

    # Milvus Host
    MILVUS_HOST :str 
    MILVUS_PORT :int 

    OCR_PORT :int 
    OCR_URL :str 


    OPENAI_API_KEY:str
    OPENAI_BASE_URL:str
    OPENAI_MODEL:str
    OPENAI_EMBEDDING_MODEL:str

    ZHIPUAI_API_KEY:str
    ZHIPUAI_MODEL: str

    SPARKAI_APP_ID:str
    SPARKAI_API_SECRET:str
    SPARKAI_API_KEY:str
    SPARKAI_DOMAIN:str
    SPARKAI_BASE_URL:str

    DOUBAOAI_API_KEY:str
    DOUBAOAI_BASE_URL:str
    DOUBAOAI_MODEL:str
    DOUBAOAI_EMBEDDING_MODEL:str
    class Config:
        env_file = ".env"
        extra = 'allow'

    # 文档存放路径
    DOCS_PATH:str = ""

    def set_docs_path(path):
        global DOCS_PATH
        DOCS_PATH = path

settings = Settings()

# print(settings.MYSQL_IP)