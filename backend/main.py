from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api import AccountRouter,ChatRouter,KnowledgeBaseRouter

from fastapi.staticfiles import StaticFiles

import uvicorn

from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "documents_stored"

from config.config import set_docs_path
import config.config


router = APIRouter()
router.include_router(AccountRouter, prefix="/account", tags=["mark", "account"])
router.include_router(ChatRouter, prefix="/chat", tags=["mark", "chat"])
router.include_router(KnowledgeBaseRouter, prefix="/knowledgebase", tags=["mark", "knowledgebase"])


app.include_router(router, prefix="/v1/api/mark", tags=["mark"])


if __name__ == "__main__":
  set_docs_path(UPLOAD_DIR)
  print(config.config.DOCS_PATH)
  config = uvicorn.Config("main:app", host="0.0.0.0", port=9988, reload=True)
  server = uvicorn.Server(config)
  server.run()