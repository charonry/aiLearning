"""
rag服务核心
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langChain.RAG.toyProject.FashionAISupport.config import config_data
from langChain.RAG.toyProject.FashionAISupport.vector_stores import VectorStores


class Rag:
    def __init__(self):
        self.vector_service = VectorStores()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
                ("human", "请回答用户提问：{input}")
            ]
        )
        self.chat_model = ChatTongyi(model=config_data.chat_model_name)
        self.chain  = self.__get_chain()


    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"

            reference_text = ""
            for doc in docs:
                reference_text += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}"
            return reference_text

        chain = ({"input":RunnablePassthrough(),"context":retriever|format_document} |
                 self.prompt_template |print_prompt| self.chat_model | StrOutputParser())
        return chain


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


if __name__ == '__main__':
    res = Rag().chain.invoke("我的体重180斤，尺码推荐")
    print(res)