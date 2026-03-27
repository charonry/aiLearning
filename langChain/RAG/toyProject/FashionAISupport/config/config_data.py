md5_path = "./resource/txt/"

# Chroma
collection_name = "fashion_ai_support"
persist_directory = "./resource/db/chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000     # 文本分割的阈值