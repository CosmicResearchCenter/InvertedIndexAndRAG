from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from paddleocr import PaddleOCR
import base64
import numpy as np
import logging
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

use_gpu = os.getenv("OCR_USE_GPU") == "False"

logger = logging.getLogger('ocr_server')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(f"OCR_USE_GPU parameter is set to {use_gpu}")

# 创建 FastAPI 应用
app = FastAPI()

# 允许所有源的CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 PaddleOCR 引擎
ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=use_gpu, show_log=False)

class OCRRequest(BaseModel):
    img64: str
    height: int
    width: int
    channels: int

@app.post("/ocr")
async def ocr_request(request: OCRRequest):
    img_file = request.img64
    height = request.height
    width = request.width
    channels = request.channels

    binary_data = base64.b64decode(img_file)
    img_array = np.frombuffer(binary_data, dtype=np.uint8).reshape((height, width, channels))
    logger.info("shape: {}".format(img_array.shape))

    # 无文件上传，返回错误
    if not img_file:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    # 调用 PaddleOCR 进行识别
    res = ocr_engine.ocr(img_array)
    logger.info("ocr result: {}".format(res))

    # 返回识别结果
    return {"results": res}

# 启动服务
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010, log_level="info")
