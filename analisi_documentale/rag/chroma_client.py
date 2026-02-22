import chromadb

from app_logger import LoggerHandler


class ChromaClient():
    """Inizializza client chromadb"""

    def __init__(self, persist_directory = "./chroma_db", collection_name="company_docs"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        self.logger = LoggerHandler().get_app_logger(__name__)

        try:
            self.logger.debug("Inizializzazione client chromadb...")
            self.client = chromadb.PersistentClient(path=self.persist_directory)

            collections = self.client.list_collections()
            collection_names = [c.name for c in collections]

            #per fini demo, elimina collection se già esiste
            if self.collection_name in collection_names:
                self.client.delete_collection(name=self.collection_name)

            self.logger.debug(f"Creazione collection {self.collection_name}...")
            self.client.create_collection(name=self.collection_name)

        except Exception as e:
            self.logger.error(f"Errore durante l'inizializzazione del client ChromaDB: {e}")
            raise Exception(f"Errore durante l'inizializzazione del client ChromaDB: {e}")

    def get_collection(self, collection_name):
        return self.client.get_collection(collection_name)
