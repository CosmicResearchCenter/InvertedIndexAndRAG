from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.chat import ChatCompletionMessage,ChatCompletionSystemMessageParam,ChatCompletionUserMessageParam,ChatCompletionAssistantMessageParam,ChatCompletionRole,ChatCompletionMessageParam
from typing import List,Iterable
from config.config import DOUBAO_API_KEY
# (type alias) ChatCompletionMessageParam: type[ChatCompletionSystemMessageParam] | type[ChatCompletionUserMessageParam] | type[ChatCompletionAssistantMessageParam] | type[ChatCompletionToolMessageParam] | type[ChatCompletionFunctionMessageParam]
from llm.llm import LLM
class DouBaoLLM(LLM):
    def __init__(self,api_key:str=DOUBAO_API_KEY) -> None:
        self.client = Ark(api_key=api_key)
        self.messages:List[Iterable[ChatCompletionMessageParam]]= []

    def setPrompt(self,prompt:str):
        message:ChatCompletionSystemMessageParam = ChatCompletionSystemMessageParam(role="system",content=prompt) 
        self.messages.append(message)
    def addHistory_User(self,content):
        message:ChatCompletionUserMessageParam = ChatCompletionUserMessageParam(role="user",content=content) 
        self.messages.append(message)
    def addHistory_Assistant(self,content):
        message:ChatCompletionAssistantMessageParam = ChatCompletionAssistantMessageParam(role="assistant",content=content)
        self.messages.append(message)
    def ChatToBot(self,content:str):
        self.addHistory_User(content)
        completion = self.client.chat.completions.create(
            model="ep-20240726180335-zb62t",
            messages = self.messages,
            stream=False,
        )
        return completion.choices[0].message.content

if __name__ == "__main__":
    doubao = DouBaoLLM()
    doubao.setPrompt("你是一个聊天助手")
    print(doubao.ChatToBot("你好"))