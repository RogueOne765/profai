import os
from app_logger import LoggerHandler
from enums import GroqModelId
from rag.rag_system import RAGSystem
from groq import Groq
from ragas.llms import llm_factory
from dotenv import load_dotenv


class RAGEvaluator:
    def __init__(self, rag_system: RAGSystem):
        if not isinstance(rag_system, RAGSystem):
            raise ValueError("rag_system must be a RAGSystem object")

        self.mon_logger = LoggerHandler().get_monitoring_logger(__name__)
        self.mon_logger.info("Starting RAGEvaluator initialization...")

        self.rag_system = rag_system

        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.mon_logger.error("GROQ_API_KEY not set")
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.llm = llm_factory(GroqModelId.OSS120.value, provider="groq", client=self.client)
