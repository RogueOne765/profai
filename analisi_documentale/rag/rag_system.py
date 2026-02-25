import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
    StorageContext,
    SimpleKeywordTableIndex,
    load_index_from_storage,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import (
    VectorIndexRetriever,
    KeywordTableSimpleRetriever,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

from app_logger import logger_instance
from rag.chroma_client import ChromaClient
from rag.custom_retriever import CustomRetriever
from utils import clean_directory


class RAGSystem():
    """
    Classe per inizializzazione RAG tramite Llamaindex
    """

    def __init__(self, documents=None, load_from_persist=False):
        """Inizializza sistema RAG"""
        self.load_from_persist = load_from_persist
        self.documents_paths = documents
        self.documents = []

        self.app_logger = logger_instance.get_app_logger(__name__)
        self.app_logger.debug(f"Inizializzazione RAGSystem (load_from_persist={load_from_persist})")

        try:
            api_key = os.getenv("GROQ_API_KEY")
            Settings.llm = Groq(model="llama3-70b-8192", api_key=api_key)

            embed_model = HuggingFaceEmbedding(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            Settings.embed_model = embed_model

            self.vector_index_id = "vector_index"
            self.keyword_index_id = "keyword_index"
            self.persist_index_dir = "./indexes"

            indexes_exists = os.path.isdir(self.persist_index_dir) and len(os.listdir(self.persist_index_dir)) > 0

            if self.load_from_persist and indexes_exists:
                self._load_from_persist()
            else:
                if not documents:
                    self.app_logger.error("No documents provided")
                    raise ValueError("No documents provided")
                self._init_from_documents()

        except Exception as e:
            self.app_logger.error(f"Errore durante inizializzazione sistema rag: {e}")
            raise Exception(f"Errore durante inizializzazione sistema rag: {e}")

    def _init_from_documents(self):
        """Inizializza RAG da zero, leggendo i documenti e creando gli indici"""
        self.app_logger.debug("Lettura dei documenti e creazione embeddings in corso...")
        os.makedirs(self.persist_index_dir, exist_ok=True)

        self.documents = SimpleDirectoryReader(input_files=self.documents_paths).load_data()

        self.chroma_client = ChromaClient()
        self.storage_context = None
        self.vector_index = None
        self._init_vector_store()

        self.retrieval = None
        self.vector_index = None
        self.keyword_index = None
        self._create_indexes()

        self.vector_retriever = None
        self.keyword_retriever = None
        self.custom_retriever = None
        self._create_retrieval()

        # rimuove eventuali file temporanei scaricati da risorse esterne
        clean_directory()

    def _load_from_persist(self):
        """Carica RAG da storage persistito"""
        self.app_logger.debug("Caricamento RAG da storage persistito...")

        self.chroma_client = ChromaClient(load_existing=True)
        self.storage_context = None
        self.vector_index = None
        self._init_vector_store()

        self.retrieval = None
        self.vector_index = None
        self.keyword_index = None
        self._load_indexes()

        self.vector_retriever = None
        self.keyword_retriever = None
        self.custom_retriever = None
        self._create_retrieval()


    def _init_vector_store(self):
        """Recupera collection e setta storage_context"""
        self.app_logger.debug("Recupero collection e creazione storage_context...")

        collection = self.chroma_client.get_collection("company_docs")
        vector_store = ChromaVectorStore(chroma_collection=collection)

        if self.load_from_persist:
            self.storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=self.persist_index_dir)
        else:
            self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

    def _create_indexes(self):
        """Inizializza indexes"""
        self.app_logger.debug("Inizializzazione vector_index e keyword_index...")

        self.vector_index = VectorStoreIndex.from_documents(
            self.documents, storage_context=self.storage_context
        )
        self.keyword_index = SimpleKeywordTableIndex.from_documents(self.documents, storage_context=self.storage_context)

        """ Persiste indexes per avvio app senza nuova elaborazione file """
        self.vector_index.set_index_id(self.vector_index_id)
        self.vector_index.storage_context.persist(persist_dir=self.persist_index_dir)
        self.keyword_index.set_index_id(self.keyword_index_id)
        self.keyword_index.storage_context.persist(persist_dir=self.persist_index_dir)

    def _load_indexes(self):
        """Carica indexes da storage persistito"""
        self.app_logger.debug("Caricamento vector_index e keyword_index da storage...")

        self.vector_index = load_index_from_storage(self.storage_context, index_id=self.vector_index_id)
        self.keyword_index = load_index_from_storage(self.storage_context, index_id=self.keyword_index_id)

    def _create_retrieval(self):
        self.app_logger.debug("Inizializzazione retriever...")
        self.vector_retriever = VectorIndexRetriever(index=self.vector_index, similarity_top_k=10)
        self.keyword_retriever = KeywordTableSimpleRetriever(index=self.keyword_index)
        self.custom_retriever = CustomRetriever(self.vector_retriever, self.keyword_retriever)

    def retrieve(self, query):
        if not query:
            return []

        return self.custom_retriever.retrieve(query)

