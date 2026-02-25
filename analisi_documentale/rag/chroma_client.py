import chromadb

from app_logger import logger_instance


class ChromaClient():
    """Inizializza client chromadb"""

    def __init__(self, persist_directory = "./chroma_db", collection_name="company_docs", load_existing=False):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.load_existing = load_existing

        self.app_logger = logger_instance.get_app_logger(__name__)

        try:
            self.app_logger.debug("Inizializzazione client chromadb...")
            self.client = chromadb.PersistentClient(path=self.persist_directory)

            collections = self.client.list_collections()
            collection_names = [c.name for c in collections]

            if self.load_existing:
                if self.collection_name not in collection_names:
                    self.app_logger.error(f"Collection {self.collection_name} not found in persisted storage")
                    raise ValueError(f"Collection {self.collection_name} not found in persisted storage")
                self.app_logger.debug(f"Caricamento collection esistente {self.collection_name}...")
            else:
                if self.collection_name in collection_names:
                    self.client.delete_collection(name=self.collection_name)
                self.app_logger.debug(f"Creazione collection {self.collection_name}...")
                self.client.create_collection(name=self.collection_name)

        except Exception as e:
            self.app_logger.error(f"Errore durante l'inizializzazione del client ChromaDB: {e}")
            raise Exception(f"Errore durante l'inizializzazione del client ChromaDB: {e}")

    def get_collection(self, collection_name):
        return self.client.get_collection(collection_name)
