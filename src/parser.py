# src/parser.py
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config


class PDFParser:
    def __init__(self):
        # 从配置类读取参数，这就是解耦的好处
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""]
        )

    def parse(self, file_path):
        """解析并清洗文本"""
        doc = fitz.open(file_path)
        raw_text = ""
        for page in doc:
            # 提取文本并进行基础清洗：去除页码、多余空格
            page_text = page.get_text()
            # 简单的去噪逻辑：去掉行首行尾空格，统一换行符
            raw_text += page_text.strip() + " "

        # 408 知识点密集，切分时要保留语义完整性
        chunks = self.splitter.split_text(raw_text)
        print(f"[INFO] PDF 解析完成，共切分为 {len(chunks)} 个知识块")
        return chunks