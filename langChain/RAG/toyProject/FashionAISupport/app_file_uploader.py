"""
文件上传web服务
运行 streamlit run .\langChain\RAG\toyProject\FashionAISupport\app_file_uploader.py
"""
import time
import streamlit as st


st.title("知识库更新服务")

uplader_file = st.file_uploader(
    "请上传文件",
    type=['txt'],
    # # False表示仅接受一个文件的上传
    accept_multiple_files=False
)

if uplader_file is not None:
    file_name = uplader_file.name
    file_type = uplader_file.type
    file_size = uplader_file.size / 1024

    st.subheader(file_name)
    st.write(f"格式：{file_type} | 大小：{file_size:.2f}KB")

    text = uplader_file.getvalue().decode("utf-8")
    st.write(text)