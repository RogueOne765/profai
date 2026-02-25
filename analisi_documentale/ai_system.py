import os
import traceback

from dotenv import load_dotenv

from dataclasses import dataclass
from typing import List

from chat.agent import ChatAgent
from app_logger import logger_instance
from rag.document_repo_client import DocumentRepositoryClient
from rag.rag_system import RAGSystem
from utils import clean_directory, is_url


@dataclass
class SystemConfig:
    repo_urls: List[str] # file pdf da scaricare per alimentare RAG
    temp_download_dir: str # directory in cui vengono salvati temporaneamente i file indicati in repo_urls
    enable_rag: bool # attiva/disabilita RAG
    load_from_persist: bool = False # carica storage perstistito per rag di runtime precedente
    max_input_tokens: int = 100 # limite token per richieste utente verso agente chat

class AISystem:
    def __init__(self, config: SystemConfig):
        if not config:
            raise ValueError("SystemConfig class must be provided")

        if config.enable_rag and (not config.temp_download_dir or not config.repo_urls):
            raise ValueError("If RAG is enabled, temp_download_dir and repo_urlsmust be provided")

        try:
            self.get_environments()

            self.app_logger = logger_instance.get_app_logger(__name__)
            self.app_logger.info("System startup...")
            self.app_logger.debug(f"Starting system with configs: {config}")

            self.config = config
            self.enable_rag = self.config.enable_rag
            self.repo_urls = self.config.repo_urls
            self.temp_download_dir = self.config.temp_download_dir

            self.rag_system = None
            self.chat_agent = None
        except Exception as e:
            raise Exception(f"Error during {__name__} instance costruction", {e})

    async def start(self):

        self.app_logger.debug("Starting execution of the startup method...")
        try:
            if self.enable_rag:
                await self.init_rag()
            self.init_agent()

        except Exception as e:
            traceback.print_exc()
            self.app_logger.error("Error during first system startup", {e})
            raise Exception("Error during first system startup", {e})

    def get_environments(self):
        """
        Verifica env prima dell'avvio dell'applicazione
        """
        load_dotenv()

        if "GROQ_API_KEY" not in os.environ:
            raise KeyError("Environment variable GROQ_API_KEY not set")

    async def init_rag(self):
        self.app_logger.debug("Starting document repository connection and rag system startup...")
        try:
            if self.config.load_from_persist:
                self.rag_system = RAGSystem(load_from_persist=self.config.load_from_persist)
            else:
                remote_urls = [url for url in self.repo_urls if is_url(url)]
                local_paths = [path for path in self.repo_urls if path not in remote_urls]
                remote_documents = []
                if len(remote_urls):
                    repo = DocumentRepositoryClient(remote_urls, temp_dir=self.temp_download_dir)
                    remote_documents = await repo.load_repository()

                self.rag_system = RAGSystem(remote_documents + local_paths, load_from_persist=self.config.load_from_persist)

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

