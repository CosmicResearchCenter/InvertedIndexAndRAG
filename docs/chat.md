### 聊天对话接口

URL: v1/api/chat/chat-message

方法: POST

请求参数:
- conversation_id: string
- message: string
- user_id: string

响应参数:

  - code: int
  - data: 
    - code
    - answer
    - Source
  - message: string

### 知识库选择接口
URL: v1/api/chat/knowledge_base

方法: POST

请求参数:
- conversation_id: string
- knowledge_base_id: string

响应参数:
  - code: int
  - data: 
    - []
  - message: string


### 清空聊天对话接口
URL: v1/api/chat/chat_clear
方法: POST
请求参数:
- conversation_id: string

响应参数:
  - code: int
  - data: 
    - []
  - message: string

### 创建知识库接口
URL: v1/api/knowledge_base
方法: POST

请求参数:
- name: string

响应参数:
  - code: int
  - data: 
    - []
  - message: string

### 知识库列表接口
URL: v1/api/knowledge_base

方法: GET

请求参数:

响应参数:
  - code: int
  - data: 
    - []
  - message: string

### 知识库详情接口
URL: v1/api/knowledge_base/{id}

方法: GET

请求参数:

响应参数:
  - code: int
  - data: 
    - []
  - message: string

### 上传文件到知识库接口
URL: v1/api/knowledge_base/{id}/upload

方法: POST

请求参数:
- file: string

响应参数:
  - code: int
  - data: 
    - []
  - message: string

### 文件索引状态接口
URL: v1/api/knowledge_base/{id}/index_status

方法: GET

请求参数:

响应参数:
  - code: int
  - data: 
    - []
  - message: string

### 聊天逻辑

用户问题 ----> 向量匹配｜模糊检索-----> 模型结合知识库信息和用户问题回答---->返回

对于历史信息，仅仅将用户问题和回答放入当前的RAG回答历史。

每次回答将回答和检索到的对应源文档返回

