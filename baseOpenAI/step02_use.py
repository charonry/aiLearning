from openai import OpenAI
import os

"""
# 获取client对象，OpenAI类对象
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "system", "content": "你是一个Python编程专家，并且不说废话简单回答"},
            {"role": "assistant", "content": "好的，我是编程专家，并且话不多，你要问什么？"},
            {"role": "user", "content": "输出hello world"}]
# 调用模型
completion = client.chat.completions.create(
    model="qwen3-max",
    messages=messages
)
# 返回数据
res = completion.choices[0].message.content
print(res)
"""

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "system", "content": "你是一个Python编程专家，并且不说废话简单回答"},
            {"role": "assistant", "content": "好的，我是编程专家，并且话不多，你要问什么？"},
            {"role": "user", "content": "输出hello world"}]

completion = client.chat.completions.create(
    model="qwen3-max",
    messages=messages,
    # 开启流式处理
    stream=True
)

for chunk in completion:
    print(chunk.choices[0].delta.content,end="~",flush=True)