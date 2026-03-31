from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool


@tool(description="获取股价，传入股票名称，返回字符串信息")
def get_price(name:str)->str:
    return f"股票{name}的价格是20元"

@tool(description="获取股票信息，传入股票名称，返回字符串信息")
def get_info(name: str) -> str:
    return f"股票{name}，是一家A股上市公司，专注于IT职业教育。"

@tool(description="获取股票干扰因素，传入股票名称，返回字符串信息")
def get_interferon(name: str) -> str:
    return f"股票{name}，就是一个干扰因素"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    # 大模型会根据用户问题和工具的 description 智能选择「最匹配」的工具，而非随机 / 全部调用。
    tools=[get_price,get_info,get_interferon],
    system_prompt="你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具"
)


for chunk in agent.stream({
    "messages":[
        # {"role": "user", "content": "传智教育股价多少，并介绍一下，还有它的干扰因素是什么"}
        {"role": "user", "content": "传智教育股价多少，并介绍一下"}
    ]
},stream_mode="values"):
    latest_message = chunk['messages'][-1]
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)
    try:
        if latest_message.tool_calls:
            print(f"工具调用：{[ tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError as e:
        pass