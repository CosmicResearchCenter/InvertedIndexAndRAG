import base64
import requests
import json
import cv2
import numpy as np
import os
# from utils.splitter.splitter import ChineseTextSplitter
# 图像文件路径
image_path = 'testimg.png'

# 使用 OpenCV 读取图像并获取尺寸和通道数
img = cv2.imread(image_path)
height, width, channels = img.shape
print(f"Image size: {width}x{height}, Channels: {channels}")

# # 确保图像是RGBA模式
# if channels != 4:
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
#     height, width, channels = img.shape
#     print(f"Converted Image size: {width}x{height}, Channels: {channels}")

# # 将图像转换为PNG格式的二进制数据
# _, binary_data = cv2.imencode('.png', img)

# 将二进制数据编码为 Base64
img64 = base64.b64encode(img).decode('utf-8')

# 构造请求数据
data = {
    "img64": img64,
    "height": height,
    "width": width,
    "channels": channels
}

# 发送 POST 请求
response = requests.post("http://127.0.0.1:8010/ocr", json=data)

# 处理响应
if response.status_code == 200:
    print("OCR Results:", response.json()['results'])
else:
    print("Error:", response.status_code, response.text)
result =response.json()['results'] 

result = [line for line in result if line]

ocr_result = [i[1][0] for line in result for i in line]

print(ocr_result)
full_dir_path = os.path.join(os.path.dirname("URL"), "tmp_files")
if not os.path.exists(full_dir_path):
    os.makedirs(full_dir_path)
filename = os.path.split("URL")[-1]
txt_file_path = os.path.join(full_dir_path, "%s.txt" % (filename))
with open(txt_file_path, 'w', encoding='utf-8') as fout:
    fout.write("\n".join(ocr_result))
# return txt_file_path
print(txt_file_path)


with open(txt_file_path) as f:
    state_of_the_union = f.read()
print(state_of_the_union)
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(        
    separator = "",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])
 
# texts_splitter = ChineseTextSplitter(pdf=False, sentence_size=300)

# print(text_splitter)

# docs = loader.load_and_split(text_splitter=texts_splitter)