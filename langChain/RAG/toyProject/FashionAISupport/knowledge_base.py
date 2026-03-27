"""
知识库
"""
import os
from langChain.RAG.toyProject.FashionAISupport.config import config_data
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

md5_file_path = os.path.join(config_data.md5_path, "md5.text")

def check_md5(md5_str:str):
    """检查传入的md5字符串是否已经被处理过了"""
    if not os.path.exists(md5_file_path):
        open(md5_file_path,'w',encoding="utf-8").close()
        return False
    else:
        with open(md5_file_path,'r',encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line == md5_str:
                    return True
        return False

def save_md5(md5_str:str):
    """将传入的md5字符串记录到文件内保存"""
    with open(md5_file_path,'a',encoding="utf-8") as f:
        f.write(md5_str + "\n")

def get_string_md5(input_str:str,encoding="utf-8"):
    """将传入的字符串转换为md5字符串"""
    # 转换成bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    # md5的16进制字符串
    md5_hex = hashlib.md5(str_bytes).hexdigest()
    return md5_hex


class KnowledgeBase:
    def __init__(self):
        os.makedirs(config_data.persist_directory,exist_ok=True)
        # 向量存储的实例
        self.chroma = Chroma(
            collection_name=config_data.collection_name,
            embedding_function=DashScopeEmbeddings(model=config_data.embedding_model_name),
            persist_directory=config_data.persist_directory,
        )
        # 文本分割器对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config_data.chunk_size,
            chunk_overlap=config_data.chunk_overlap,
            separators=config_data.separators,
            length_function=len
        )

    def upload_by_str(self,data:str,filename):
        """将传入的字符串进行向量化，存入向量数据库中"""
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        if len(data) > config_data.max_split_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "charon",
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)
        return "[成功]内容已经成功载入向量库"



if __name__ == '__main__':
    # md5 = get_string_md5("炒股要发财")
    # print(md5)
    # save_md5(md5)
    # print(check_md5(md5))
    service = KnowledgeBase()
    r = service.upload_by_str("测试[]list有无在数据库区别","炒股")
    print(r)
