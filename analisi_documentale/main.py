import os
from dotenv import load_dotenv
import asyncio
import traceback
from document_repo_client import DocumentRepositoryClient
from rag.rag_system import RAGSystem
from agent import ChatAgent
from utils import clean_directory

load_dotenv()

async def start_system(repo_urls, temp_download_dir):
    try:

        """
        Setta env per api groq
        """
        if "GROQ_API_KEY" not in os.environ:
            raise KeyError("Environment variable GROQ_API_KEY not set")

        """
        Avvia RAG e download file di demo.
        """
        repo = DocumentRepositoryClient(repo_urls, temp_dir=temp_download_dir)
        documents = await repo.load_repository()
        rag = RAGSystem(documents)
        repo.cleanup_temp_files()

        """
        Avvia chatbot
        """
        agent = ChatAgent(rag)
        agent.start_chatbot()

    except Exception as e:
        clean_directory()
        traceback.print_exc()
        print(f"Errore durante inizializzazione sistema: {e}")
        return


if __name__ == '__main__':

    urls = [
        "https://backoffice.lumsa.it/sites/default/files/file/3564/2024-06/Guida-per-lo-studente_12giugno_WEB_240612_113324.pdf",
        "https://backoffice.lumsa.it/sites/default/files/file/4252/2025-03/Linee%20guida%20prova%20finale%20LMG-01%20febbraio%202025.pdf",
        "https://backoffice.lumsa.it/sites/default/files/file/6/2023-07/Indicazioni%20tirocinio%20LM%2059.pdf",
        "https://backoffice.lumsa.it/sites/default/files/file/3564/2025-07/ELENCO%20ENTI%20CONVENZIONATI%20TIROCINIO.pdf"
    ]
    tmp_dir = "temp_downloads"
    asyncio.run(start_system(urls, tmp_dir))
