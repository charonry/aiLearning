from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import (before_agent, after_agent, before_model, after_model,
    wrap_model_call, wrap_tool_call)
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime
"""
middleware：对智能体的每一步工作进行控制和自定义的执行。
    通过Hooks钩子来实现拦截，自定义中间件可以简单的使用装饰器来定义。
"""

@tool(description="查询天气，传入城市名称字符串，返回字符串天气信息")
def get_weather(city: str) -> str:
    return f"{city}天气：晴天"

# 节点式钩子
@before_agent
def log_before_agent(state:AgentState,runtime:Runtime)->None:
    print(f"[before agent]agent启动，并附带{len(state['messages'])}消息")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent]agent结束，并附带{len(state['messages'])}消息")

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before_model]模型即将调用，并附带{len(state['messages'])}消息")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after_model]模型调用结束，并附带{len(state['messages'])}消息")


# 包装式钩子
@wrap_model_call
def model_call_hook(request,handler):
    print("模型调用啦")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request,handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行传入参数：{request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    middleware=[log_before_agent,log_after_agent,log_before_model,log_after_model,
                model_call_hook,tool_call_hook]
)

res = agent.invoke({"messages":[{"role": "user", "content": "明天深圳的天气如何？如何穿衣"},]})
print("*"*30)
for msg in res["messages"]:
    print(type(msg).__name__,msg.content)