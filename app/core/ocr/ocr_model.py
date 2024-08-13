import base64
import requests
import json
import cv2
import numpy as np
import os
from paddleocr import PaddleOCR

class OCR_Model:
    def __init__(self,ocr_server_base:str,ocr_server_port:int) -> None:
        self.ocr_server_base = ocr_server_base
        self.ocr_server_port = ocr_server_port

    def get_ocr_server(self,request_data):
        response = requests.post(f"{self.ocr_server_base}:{self.ocr_server_port}/ocr", json=request_data)    
        # 处理响应
        if response.status_code == 200:
            result =response.json()['results'] 

            result = [line for line in result if line]

            ocr_result = [i[1][0] for line in result for i in line]
            return "\n".join(ocr_result)
        else:
            print("Error:", response.status_code, response.text)
     
    def ocr_image_by_file(self,image_path:str):
        img = cv2.imread(image_path)
        height, width, channels = img.shape
        img64 = base64.b64encode(img).decode('utf-8')
        # 构造请求数据
        data = {
            "img64": img64,
            "height": height,
            "width": width,
            "channels": channels
        }
        
        return self.get_ocr_server(data) 
        
    def ocr_image_by_image_bytes(self,image_bytes:str) -> str:
        # 将二进制数据转换为NumPy数组
        image_array = np.frombuffer(image_bytes, np.uint8)
        
        # 使用OpenCV将NumPy数组解码为图像
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        height, width, channels = image.shape
        img64 = base64.b64encode(image).decode('utf-8')
        # 构造请求数据
        data = {
            "img64": img64,
            "height": height,
            "width": width,
            "channels": channels
        }
        return self.get_ocr_server(data) 
if __name__ == '__main__':
    ocr_model = OCR_Model("http://127.0.0.1",8010)
    image_path = "/Users/markyangkp/Desktop/Projects/llmqa/ocr/testimg.png"
    ocr_result = ocr_model.ocr_image_by_file(image_path)
    print(type(ocr_result))
    print(ocr_result)