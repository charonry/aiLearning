"""
向量存储
"""
from langchain_chroma import Chroma
from langChain.RAG.toyProject.FashionAISupport.config import config_data
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStores:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=config_data.collection_name,
            embedding_function=DashScopeEmbeddings(model=config_data.embedding_model_name),
            persist_directory=config_data.persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config_data.similarity_threshold})



if __name__ == "__main__":
    vector_stores = VectorStores()
    retriever = vector_stores.get_retriever()
    res = retriever.invoke("我的体重180斤，尺码推荐")
    print(res)

