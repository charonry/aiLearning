"""
langchain的ChatPromptTemplate提示词模板
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗")
    ]
)

history_data = [
    ("human", "你来写一个唐诗"),
    ("ai", "床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午，汗滴禾下锄，谁知盘中餐，粒粒皆辛苦"),
]
model = ChatTongyi(model="qwen3-max")
# 方式一：模版注入
"""
# 只能是invoke方法
prompt_text = chat_prompt_template.invoke({"history":history_data})

res = model.invoke(prompt_text)
print(res.content,type(res))
"""
# 方式二：chain链
chain = chat_prompt_template | model
res = chain.invoke({"history":history_data})
print(res.content,type(res))