"""
langchain的聊天模型调用
"""
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

"""
messages = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，在写一首唐诗。")
]
"""
# 简写 （角色，内容）
messages = [
    ("system", "你是一个边塞诗人。"),
    ("human", "写一首唐诗。"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照你上一个回复的格式，在写一首唐诗。")
]

model = ChatTongyi(model="qwen3-max")

# model = ChatOllama(model="qwen3:4b")

res = model.stream(messages)
for chunk in res:
    # .content来获取输出内容
    print(chunk.content, end="", flush=True)