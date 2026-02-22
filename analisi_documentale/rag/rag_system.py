from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
    StorageContext,
    SimpleKeywordTableIndex,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import (
    VectorIndexRetriever,
    KeywordTableSimpleRetriever,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from app_logger import logger_instance
from rag.chroma_client import ChromaClient
from rag.custom_retriever import CustomRetriever

class RAGSystem():
    """
    Classe per inizializzazione RAG tramite Llamaindex
    """

    def __init__(self, documents):
        """Inizializza sistema RAG"""
        if not documents:
            raise ValueError("No documents provided")
        self.document_path_list = documents
        self.documents = []

        self.app_logger = logger_instance.get_app_logger(__name__)
        self.app_logger.debug(f"Inizializzazione RAGSystem su {len(documents)} documenti")

        try:
            """
            La classe SimpleKeywordTableIndex durante inizializzazione cerca api key di llm default per langchain (open ai)
            Disabilitato per evitare che sollevi eccezione
            """
            Settings.llm = None

            # setta embedding model
            embed_model = HuggingFaceEmbedding(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            Settings.embed_model = embed_model

            # Legge i file
            self.app_logger.debug("Lettura dei documenti e creazione embeddings in corso...")
            self.documents = SimpleDirectoryReader(input_files=self.document_path_list).load_data()

            # inizializzazione db vettoriale
            self.chroma_client = ChromaClient()
            self.storage_context = None
            self.vector_index = None
            self._init_vector_store()

            #inizializza index
            self.retrieval = None
            self.vector_index = None
            self.keyword_index = None
            self._create_indexes()

            # inizializza retriever custom
            self.vector_retriever = None
            self.keyword_retriever = None
            self.custom_retriever = None
            self._create_retrieval()


        except Exception as e:
            raise Exception(f"Errore durante inizializzazione sistema rag: {e}")


    def _init_vector_store(self):
        """Recupera collection e setta storage_context"""
        self.app_logger.debug("Recupero collection e creazione storage_context...")

        collection = self.chroma_client.get_collection("company_docs")
        vector_store = ChromaVectorStore(chroma_collection=collection)

        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

    def _create_indexes(self):
        """Inizializza indexes"""
        self.app_logger.debug("Inizializzazione vector_index e keyword_index...")

        self.vector_index = VectorStoreIndex.from_documents(
            self.documents, storage_context=self.storage_context
        )
        self.keyword_index = SimpleKeywordTableIndex.from_documents(self.documents, storage_context=self.storage_context)

    def _create_retrieval(self):
        self.app_logger.debug("Inizializzazione retriever...")
        self.vector_retriever = VectorIndexRetriever(index=self.vector_index, similarity_top_k=10)
        self.keyword_retriever = KeywordTableSimpleRetriever(index=self.keyword_index)
        self.custom_retriever = CustomRetriever(self.vector_retriever, self.keyword_retriever)

    def retrieve(self, query):
        if not query:
            return []

        return self.custom_retriever.retrieve(query)

