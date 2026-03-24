"""
langchain的嵌入模型调用
"""
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_ollama import OllamaEmbeddings

# 创建模型对象 不传model默认用的是 text-embeddings-v1
# model = DashScopeEmbeddings()
model = OllamaEmbeddings(model="qwen3-embedding:4b")

res_query = model.embed_query("continue插件")
# text-embedding-v1:1536    qwen3-embedding:4b:2560
print(len(res_query),res_query)
res_doc = model.embed_documents(['continue插件','pycharm','使用'])
# 3*1536 2560
print(len(res_doc[0]),res_doc)

