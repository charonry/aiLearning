"""
langchain的基础使用
1.调用qwen-max大模型
2.调用本地ollama模型：qwen3:4b
"""
# 调用云端模型
"""
from langchain_community.llms.tongyi import Tongyi
# 创建选择模型
model = Tongyi(model="qwen-max")
# 调用模型
res = model.invoke("你是谁，具体是哪个型号模型")
print(res)
"""
# 调用本地模型
from langchain_ollama import OllamaLLM
model = OllamaLLM(model="qwen3:4b")
# invoke:一次性返回  stream：流式输出
res = model.stream(input="你是谁，具体是哪个型号模型，与qwen-max有什么区别")
for chunk in res:
    print(chunk,end="",flush=True)