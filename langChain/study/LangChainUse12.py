"""
向量存储
"""

# 内部向量临时化存储
"""
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader


loader = CSVLoader(
    encoding="utf-8",
    file_path="./resource/csv/info.csv",
    source_column="source"
)
documents = loader.load()

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)
# 向量存储的新增
vector_store.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1,len(documents)+1)]
)

# 删除
vector_store.delete(["id1","id2"])

# 检索
result = vector_store.similarity_search(
    "python学习哪些知识",
    3
)
print(result)
"""

# 外部向量持久化存储
"""
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# loader = CSVLoader(
#     encoding="utf-8",
#     file_path="./resource/csv/info.csv",
#     source_column="source"
# )
# documents = loader.load()

vector_store = Chroma(
    # 当前向量存储起个名字，类似数据库的表名称
    collection_name="info",
    embedding_function=DashScopeEmbeddings(),
    # 指定数据存放的文件夹
    persist_directory="./resource/db/chroma_db"
)
# 向量存储的新增
# vector_store.add_documents(
#     documents=documents,
#     ids=["id"+str(i) for i in range(1,len(documents)+1)]
# )

# 删除
# vector_store.delete(["id1","id2"])

# 检索
result = vector_store.similarity_search(
    "python学习哪些知识",
    3,
    # 增加过滤条件
    filter={"source":"黑马程序员"}
)
print(result)
"""

# 向量检索构建提示词
"""
import os
from langchain_community.chat_models import ChatTongyi
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print(prompt.to_string())
    print("=" * 20)
    return prompt


model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问：{input}")
    ]
)

# 因为维度不一样会报错，采用模型是不一致的 默认：text-embedding-v1
# embedding = DashScopeEmbeddings(model="text-embedding-v4",dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))
embedding = DashScopeEmbeddings()
vector_store = Chroma(
    # 当前向量存储起个名字，类似数据库的表名称
    collection_name="info",
    embedding_function=embedding,
    # 指定数据存放的文件夹
    persist_directory="./resource/db/chroma_db"
)

input_text = "学习python的好处"

result = vector_store.similarity_search(input_text, 4)
reference_text = "["
for doc in result:
    content = doc.page_content
    info = content.split("info: ")[1]+","
    reference_text += info
reference_text = reference_text[:-1] + "]"

chain = prompt | print_prompt | model | StrOutputParser()
res = chain.invoke({"input": input_text, "context": reference_text})
print(res)
"""

# 向量检索入链
from langchain_community.chat_models import ChatTongyi
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough

def print_prompt(prompt):
    print(prompt.to_string())
    print("=" * 20)
    return prompt


model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问：{input}")
    ]
)

embedding = DashScopeEmbeddings()
vector_store = Chroma(
    collection_name="info",
    embedding_function=embedding,
    persist_directory="./resource/db/chroma_db"
)

input_text = "学习python的好处"

# langchain中向量存储对象，有一个方法：as_retriever，可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k":4})

def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"

    reference_text = "["
    for doc in docs:
        content = doc.page_content
        info = content.split("info: ")[1] + ","
        reference_text += info
    reference_text = reference_text[:-1] + "]"
    return reference_text

chain = {"input":RunnablePassthrough(),"context":retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
res = chain.invoke(input_text)
print(res)