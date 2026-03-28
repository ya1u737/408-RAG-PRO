# 🎓 408-RAG-Pro: 基于本地 LLM 的计算机考研智能辅导助手

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-orange.svg)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green.svg)

## 🌟 项目简介
这是一个专为 **408 计算机考研**（数据结构、操作系统、计组、计网）设计的 RAG（检索增强生成）系统。
不同于通用的 PDF 助手，本项目通过**结构化 Prompt 工程**与**模块化架构**，深度对齐 408 考纲要求，提供精准的术语解析与 C++ 代码示范。

## 🏗️ 核心架构
项目采用**解耦设计**，确保每一层逻辑的可扩展性：
- **Config**: 集中化管理模型参数与检索阈值。
- **Parser**: 基于 PyMuPDF 的文本清洗与分段策略。
- **Retriever**: 向量存储与语义检索，支持检索分数过滤。
- **Generator**: 针对 408 场景优化的结构化提示词引擎。

## 🛠️ 技术栈
- **LLM**: Ollama (Qwen2 / Llama3)
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit

## 🚀 快速开始
1. **克隆项目**:
   ```bash
   git clone [https://github.com/你的用户名/408-RAG-Pro.git](https://github.com/你的用户名/408-RAG-Pro.git)
   cd 408-RAG-Pro