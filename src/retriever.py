# src/retriever.py
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from src.config import Config

class KnowledgeBase:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=Config.EMBED_MODEL)
        # 初始化数据库，指定持久化路径
        self.vectorstore = Chroma(
            persist_directory=Config.DB_PATH,
            embedding_function=self.embeddings
        )

    def add_documents(self, texts):
        """将清洗后的文本块加入向量库"""
        self.vectorstore.add_texts(texts=texts)
        print(f"[INFO] 已存入数据库，路径: {Config.DB_PATH}")

    def search(self, query):
        """带分数的语义检索"""
        # 检索 Top K 个最相关的片段
        docs_with_scores = self.vectorstore.similarity_search_with_relevance_scores(
            query, k=Config.TOP_K
        )
        # 过滤掉低于 0.4 分的无关内容（防止 AI 瞎编）
        relevant_docs = [doc for doc, score in docs_with_scores if score > 0.4]
        return relevant_docs