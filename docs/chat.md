### 聊天对话接口

URL: v1/api/chat
方法: POST
请求参数:
- conversation_id: string
- message: string

响应参数:

  - code: int
  - data: 
    - code
    - answer
    - Source
  - message: string



### 聊天逻辑

用户问题 ----> 向量匹配｜模糊检索-----> 模型结合知识库信息和用户问题回答---->返回

对于历史信息，仅仅将用户问题和回答放入当前的RAG回答历史。

每次回答将回答和检索到的对应源文档返回

