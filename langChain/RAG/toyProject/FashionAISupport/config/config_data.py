# md5加密文件父路径
md5_path = "./resource/txt/"

# 嵌入模型
embedding_model_name = "text-embedding-v4"
# 聊天模型
chat_model_name = "qwen3-max"

# Chroma
collection_name = "fashion_ai_support"
persist_directory = "./resource/db/chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000     # 文本分割的阈值

# 向量检索返回匹配的文档数量
similarity_threshold = 1