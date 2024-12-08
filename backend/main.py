from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api import AccountRouter,ChatRouter,KnowledgeBaseRouter,AdminRouter

origins = [
    "*"
]


from fastapi.staticfiles import StaticFiles

import uvicorn

from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 允许的域名
    allow_credentials=True,           # 允许携带凭证
    allow_methods=["*"],              # 允许的 HTTP 方法，如 GET, POST 等
    allow_headers=["*"],              # 允许的请求头
)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "documents_stored"

from config.config import set_docs_path
import config.config
set_docs_path(UPLOAD_DIR)

router = APIRouter()
router.include_router(AccountRouter, prefix="/account", tags=["mark", "account"])
router.include_router(ChatRouter, prefix="/chat", tags=["mark", "chat"])
router.include_router(KnowledgeBaseRouter, prefix="/knowledgebase", tags=["mark", "knowledgebase"])
router.include_router(AdminRouter, prefix="/admin", tags=["mark", "admin"])

app.include_router(router, prefix="/v1/api/mark", tags=["mark"])


if __name__ == "__main__":
  
  print(config.config.DOCS_PATH)
  config = uvicorn.Config("main:app", host="0.0.0.0", port=9988, reload=True)
  server = uvicorn.Server(config)
  server.run()