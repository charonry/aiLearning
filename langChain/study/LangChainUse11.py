"""
文档加载器(Document loaders)
"""
# CSVLoader
"""
from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(
    encoding="utf-8",
    file_path="./resource/csv/stu.csv",
    csv_args={
        "delimiter": ",",       # 指定分隔符
        "quotechar": '"',       # 指定带有分隔符文本的引号包围是单引号还是双引号
        # 如果数据原本有表头，就不要下面的代码，如果没有可以使用
        "fieldnames": ['name', 'age', 'gender', '爱好']
    }
)
# documents = loader.load()
# for document in documents:
#     print(document,type(document))
for document in  loader.lazy_load():
    print(document, type(document))
"""

# JSONLoader
"""
from langchain_community.document_loaders import JSONLoader
import json
loader = JSONLoader(
    file_path="./resource/json/stu_json_lines.json",
    jq_schema=".",
    text_content=False,  # 告知JSONLoader 我抽取的内容不是字符串 默认True
    json_lines=True  # 告知JSONLoader 这是一个JSONLines文件（每一行都是一个独立的标准JSON） 默认False
)
for document in loader.lazy_load():
    raw_content = document.page_content
    data = json.loads(raw_content)
    document.page_content = json.dumps(data, ensure_ascii=False)
    print(type(document),document)
"""

# TextLoader
"""
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(r"./resource/txt/Python基础语法.txt",encoding="utf-8")
# 整个文件加载成 1 个 Document 对象
document = loader.lazy_load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 分段的最大字符数
    chunk_overlap=50,   # 分段之间允许重叠字符数
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],   # 文本自然段落分隔的依据符号
    length_function=len,    # 统计字符的依据函数
)

split_docs = splitter.split_documents(document)
print(len(split_docs))
for doc in split_docs:
    print("="*20)
    print(doc)
    print("="*20)
"""


# PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(
    file_path=r"./resource/pdf/pdf2.pdf",
    # 默认是page模式，每个页面形成一个Document文档对象，
    # single模式，不管有多少页，只返回1个Document对象
    mode="page",
    password="itheima"
)
i = 0
for doc in loader.lazy_load():
    i += 1
    print(doc,f"====={i}" )
