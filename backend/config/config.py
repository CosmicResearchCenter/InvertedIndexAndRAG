from config.splitter_model import SplitterModel
# OpenAI的BaseURL
OPENAI_BASE_URL = "https://aihubmix.com/v1"

# OpenAI的API_KEY
OPENAI_API_KEY = "sk-i2dHdOeKiGt9wA2G853b4dC10aEc419a9051F3C69e86284b"

# 豆包的API_KEY
DOUBAO_API_KEY = "d42e75b4-a5ef-4e9a-90ed-d93a9dcc2966"

LLM_MODEL = "gpt-4o-mini"

# 拆分形式 默认LLM拆分
SPPLITTER_MODEL = SplitterModel.LLMSplitter

# OCR
## OCR_PORT
OCR_PORT = 8010
OCR_URL = "http://127.0.0.1"

# Embedding
EMBEDDING_MODEL_PROVIDER = "openai"


# ES_BASE_URL
ES_BASE_URL = "222.199.255.41"
ES_BASE_PORT = 9200

# Milvus Host
MILVUS_HOST = "222.199.255.41"
MILVUS_PORT = 19530

# 文档存放路径
DOCS_PATH = ""

def set_docs_path(path):
    global DOCS_PATH
    DOCS_PATH = path