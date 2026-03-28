# app.py
import streamlit as st
import os
from src.config import Config
from src.parser import PDFParser
from src.retriever import KnowledgeBase
from src.generator import AnswerGenerator
st.set_page_config(
    page_title="408 RAG Pro",
    page_icon="🎓",
    layout="centered", # 居中布局比全屏更像一个专业工具
    initial_sidebar_state="expanded"
)
# --- 1. 初始化所有组件 (放到 session_state 里防止重复加载) ---
if "parser" not in st.session_state:
    st.session_state.parser = PDFParser()
    st.session_state.kb = KnowledgeBase()
    st.session_state.generator = AnswerGenerator()

st.set_page_config(page_title="408 RAG Pro", layout="wide")
st.title("🎓 408 考研智能导师 (大手子版）")

# --- 2. 侧边栏：知识库管理 ---
with st.sidebar:
    st.header("📂 资料入库")
    uploaded_file = st.file_uploader("上传 408 PDF 讲义", type="pdf")

    if uploaded_file and st.button("开始向量化解析"):
        # 确保目录存在
        os.makedirs(Config.DATA_PATH, exist_ok=True)
        file_path = os.path.join(Config.DATA_PATH, "temp.pdf")

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("正在解析并构建向量索引..."):
            chunks = st.session_state.parser.parse(file_path)
            st.session_state.kb.add_documents(chunks)
            st.success("入库成功！现在可以开始提问了。")

# --- 3. 主界面：智能问答 ---
if prompt := st.chat_input("输入你的 408 问题，如帮我复习一下kmp算法......"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # A. 检索 (Retriever)
        relevant_docs = st.session_state.kb.search(prompt)

        # B. 思考过程展示 (展现你的技术透明度)
        with st.expander("🔍 检索溯源 "):
            if not relevant_docs:
                st.warning("未匹配到相关资料，将开启纯模型回答模式。")
            for i, doc in enumerate(relevant_docs):
                st.markdown(f"**片段 {i + 1}:** {doc.page_content[:200]}...")

        # C. 生成答案 (Generator)
        response_stream = st.session_state.generator.generate(prompt, relevant_docs)
        st.write_stream(response_stream)