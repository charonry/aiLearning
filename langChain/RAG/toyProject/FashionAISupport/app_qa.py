"""
页面QA

运行 python -m streamlit run .\langChain\RAG\toyProject\FashionAISupport\app_qa.py
"""
import time
import streamlit as st
from langChain.RAG.toyProject.FashionAISupport.rag import Rag
from langChain.RAG.toyProject.FashionAISupport.config import config_data

st.title("智能客服")
st.divider()

msg = st.chat_input()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = Rag()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

if msg:
    st.chat_message("user").write(msg)
    st.session_state["message"].append({"role": "user", "content": msg})

    with st.spinner("AI思考中..."):
        # time.sleep(1)
        res = st.session_state["rag"].chain.stream({"input":msg},config_data.session_config_id)
        res_back = st.chat_message("assistant").write_stream(res)
        st.session_state["message"].append({"role": "assistant", "content": res_back})