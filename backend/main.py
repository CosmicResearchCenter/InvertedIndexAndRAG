from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api import AccountRouter,ChatRouter,KnowledgeBaseRouter

from fastapi.staticfiles import StaticFiles

import uvicorn


app = FastAPI()



router = APIRouter()
router.include_router(AccountRouter, prefix="/account", tags=["mark", "account"])
router.include_router(ChatRouter, prefix="/chat", tags=["mark", "chat"])
router.include_router(KnowledgeBaseRouter, prefix="/knowledgebase", tags=["mark", "knowledgebase"])


app.include_router(router, prefix="/v1/api/mark", tags=["mark"])


if __name__ == "__main__":
  config = uvicorn.Config("main:app", host="0.0.0.0", port=9988, reload=True)
  server = uvicorn.Server(config)
  server.run()