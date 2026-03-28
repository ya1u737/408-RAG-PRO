# src/generator.py
from langchain_ollama import ChatOllama
from src.config import Config


class AnswerGenerator:
    def __init__(self):
        # 这里的模型名直接从 Config 读取，以后改模型只需动 config.py
        self.llm = ChatOllama(
            model=Config.CHAT_MODEL,
            temperature=0.3,  # 考研题要严谨，温度开低点
            streaming=True  # 开启流式输出，用户体验拉满
        )

    def generate(self, question, context_docs):
        """
        核心逻辑：把检索到的知识块拼进 Prompt 模板
        """
        # 1. 提取文本内容
        context_text = "\n\n".join([doc.page_content for doc in context_docs])

        # 2. 填充模板（这部分以后可以根据不同科目在 Config 里换）
        prompt = Config.PROMPT_TEMPLATE.format(
            context=context_text,
            question=question
        )

        # 3. 调用大模型（流式返回，省得用户等半天）
        return self.llm.stream(prompt)