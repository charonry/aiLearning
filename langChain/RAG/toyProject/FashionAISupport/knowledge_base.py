"""
知识库
"""
import os
from langChain.RAG.toyProject.FashionAISupport.config.config_data import md5_path
import hashlib

file_path = os.path.join(md5_path, "md5.text")

def check_md5(md5_str:str):
    """检查传入的md5字符串是否已经被处理过了"""
    if not os.path.exists(file_path):
        open(file_path,'w',encoding="utf-8").close()
        return False
    else:
        with open(file_path,'r',encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line == md5_str:
                    return True
        return False

def save_md5(md5_str:str):
    """将传入的md5字符串记录到文件内保存"""
    with open(file_path,'a',encoding="utf-8") as f:
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
        # 向量存储的实例
        self.chroma = None
        # 文本分割器对象
        self.spliter = None

    def upload_by_str(self,data,filename):
        """将传入的字符串进行向量化，存入向量数据库中"""
        pass


if __name__ == '__main__':
    md5 = get_string_md5("炒股要发财")
    print(md5)
    save_md5(md5)
    print(check_md5(md5))
