# from openai import OpenAI

# base_url = "https://oneapi.k.cn:8443/v1"
# model = "qwen2-instruct"

# messages = [
#     {"role": "system", "content": "你是一个聊天助手"},
#     {"role": "user", "content": "你是谁？"},
# ]
# openai = OpenAI(
#         base_url=base_url,
#         api_key="sk-Td6hjVG6CqOuWtC7DfA233D083534b51912d4608Ee492565",
#                 )

# res = openai.chat.completions.create(
#             max_tokens=1024,
#             model=model ,
#             messages=messages,
            
#         )
# print(res.choices[0].message.content)

import requests
import os

# API配置
api_key = "sk-Td6hjVG6CqOuWtC7DfA233D083534b51912d4608Ee492565"  # 从环境变量获取API密钥
url = "https://oneapi.k.cn:8443/v1/chat/completions"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# 请求体
data = {
    "model": "qwen2-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
}

# 发送POST请求
response = requests.post(url, headers=headers, json=data, verify=False)

# 输出结果
if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)