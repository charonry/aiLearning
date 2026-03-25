"""
langchain的StrOutputParser解析器
StrOutputParser是LangChain内置的简单字符串解析器。
    可以将AIMessage解析为简单的字符串，符合了模型invoke方法要求（可传入字符串，不接收AIMessage类型）；
    是Runnable接口的子类（可以加入链）。
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model="qwen3-max")
prompt_template = PromptTemplate.from_template("你叫{name}，年龄{age},你觉得你会是什么样子个性")
# ValueError: Invalid input type <class 'langchain_core.messages.ai.AIMessage'>. Must be a PromptValue, str, or list of BaseMessages.
parser = StrOutputParser()
chain_1 = prompt_template | model | parser | model
res_1 = chain_1.invoke({"name": "prompt", "age": "18"})
print(res_1.content,type(res_1))
print("*"*50)
chain_2 = prompt_template | model | parser | model | parser
res_2:str = chain_2.invoke({"name": "prompt", "age": "18"})
print(res_2,type(res_2))