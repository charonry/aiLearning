"""
JsonOutputParser解析器：
AIMessage  Dict(JSON)
RunnableLambda：
是LangChain内置的，将普通函数等转换为Runnable接口实例，方便自定义函数加入chain
"""
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# 模型创建
model = ChatTongyi(model="qwen3-max")

# 创建所需的解析器
parser_str = StrOutputParser()

# 方式一：JsonOutputParser
"""
parser_json = JsonOutputParser()

prompt_first = PromptTemplate.from_template("我叫{name}，年龄{age},你觉得我会是什么样子个性，"
               "并封装为JSON格式返回给我。要求key是character，value就是你的答案，请严格遵守格式要求。")
prompt_second = PromptTemplate.from_template("个性：{character}，这是你对我的分析，你觉得对吗？")

chain = prompt_first | model | parser_json
# res = chain.invoke({"name": "charon", "age": "18"})
# print(res,type(res))
chain = prompt_first | model | parser_json | prompt_second | model | parser_str
for chunk in chain.stream({"name": "charon", "age": "18"}):
    print(chunk, end="", flush=True)
"""

# 方式二：RunnableLambda
prompt_first = PromptTemplate.from_template("我叫{name}，年龄{age},你觉得我会是什么个性，简单回答")
prompt_second = PromptTemplate.from_template("个性：{character}，这是你对我的分析，你觉得你分析对吗")
# my_func = RunnableLambda(lambda msg:{"character":msg.content})
# chain = prompt_first | model | my_func
# res = chain.invoke({"name": "charon", "age": "18"})
# print(res,type(res))
chain = prompt_first | model | (lambda msg:{"character":msg.content}) | prompt_second | model | parser_str
for chunk in chain.stream({"name": "charon", "age": "18"}):
    print(chunk, end="", flush=True)