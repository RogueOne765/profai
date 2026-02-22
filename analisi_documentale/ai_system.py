import os
import traceback

from dotenv import load_dotenv

from dataclasses import dataclass
from typing import List

from chat.agent import ChatAgent
from app_logger import logger_instance
from rag.document_repo_client import DocumentRepositoryClient
from rag.rag_system import RAGSystem
from utils import clean_directory


@dataclass
class SystemConfig:
    repo_urls: List[str]
    temp_download_dir: str
    enable_rag: bool
    max_input_tokens: int = 100

class AISystem:
    def __init__(self, config: SystemConfig):
        if not config:
            raise ValueError("SystemConfig class must be provided")

        if config.enable_rag and (not config.temp_download_dir or not config.repo_urls):
            raise ValueError("If RAG is enabled, temp_download_dir and repo_urlsmust be provided")

        self.app_logger = logger_instance.get_app_logger(__name__)
        self.app_logger.info("System startup...")
        self.app_logger.debug(f"Starting system with configs: {config}")

        self.config = config
        self.enable_rag = self.config.enable_rag
        self.repo_urls = self.config.repo_urls
        self.temp_download_dir = self.config.temp_download_dir

        self.rag_system = None
        self.chat_agent = None

    async def start(self):

        self.app_logger.debug("Starting execution of the startup method...")
        try:
            self.get_environments()
            if self.enable_rag:
                await self.init_rag()
            self.init_agent()

        except Exception as e:
            traceback.print_exc()
            self.app_logger.error("Error during first system startup", {e})
            raise Exception("Error during first system startup", {e})

    def get_environments(self):
        """
        Setta env per api groq
        """
        self.app_logger.debug("Validating environments...")

        load_dotenv()

        if "GROQ_API_KEY" not in os.environ:
            raise KeyError("Environment variable GROQ_API_KEY not set")

    async def init_rag(self):
        self.app_logger.debug("Starting document repository connection and rag system startup...")
        try:
            repo = DocumentRepositoryClient(self.repo_urls, temp_dir=self.temp_download_dir)
            documents = await repo.load_repository()
            self.rag_system = RAGSystem(documents)
            repo.cleanup_temp_files()
        except Exception as e:
            clean_directory()
            raise Exception("Error during first RAG system startup", {e})

    def init_agent(self):
        """
        Avvia chatbot
        """
        try:
            agent = ChatAgent(rag_system=self.rag_system, max_input_tokens=self.config.max_input_tokens)
            agent.start_chatbot()
        except Exception as e:
            raise Exception("Error during Chat Agent startup", {e})

