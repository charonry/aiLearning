"""
langchain的通用提示词模板
zero-shot：可以基于PromptTemplate直接完成
"""
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-max")
# 通用提示词模板
prompt_template = PromptTemplate.from_template("你叫{name}，年龄{age},你觉得你会是什么样子个性")

# 方式一：模版注入
"""
# 调用.format方法注入信息
prompt_text = prompt_template.format(name="prompt",age="5")
res = model.invoke(prompt_text)
"""

# 方式二: chain执行链条
"""
chain = prompt_template | model
res = chain.invoke({"name":"prompt","age":"5"})
print(res)
"""

# format和invoke的区别
prompt_format = prompt_template.format(name="prompt",age="5")
print(prompt_format,type(prompt_format))
prompt_invoke = prompt_template.invoke({"name":"prompt","age":"5"})
print(prompt_invoke,type(prompt_invoke))