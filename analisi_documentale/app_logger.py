import os
import logging
from logging.handlers import RotatingFileHandler

class LoggerHandler:
    """
    Gestione logging handler con singleton per utilizzo tra le varie classi dell'applicazione
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        """
        Livelli di profondità dei log sono definiti tramite variabile ambiente
        per distinguere staging/produzione
        """
        self.env = os.getenv("APP_ENV", "production")  # "staging" | "production"
        self.log_levels = {
            "staging": logging.DEBUG,
            "production": logging.WARNING,
        }

        self.level = self.log_levels[self.env] if self.env else logging.DEBUG

        """
        Definisce e Crea directory destinazione file di log
        """

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.app_log_dir = os.path.join(self.base_dir, "logs", "app")
        os.makedirs(self.app_log_dir, exist_ok=True)
        self.llm_log_dir = os.path.join(self.base_dir, "logs", "llm")
        os.makedirs(self.llm_log_dir, exist_ok=True)

        self._initialized = True


    def get_app_logger(self, name="app_global"):
        """
        Inizializza logger per aggiornare utente su stato sistema
        """
        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(self.level)

        rotating_handler = RotatingFileHandler(
            os.path.join(self.app_log_dir, "app.log"),
            maxBytes=1000000,
            backupCount=5
        )

        log_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s \n'
        )

        rotating_handler.setFormatter(log_format)
        logger.addHandler(rotating_handler)

        if self.env != "production":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            logger.addHandler(console_handler)

        return logger


    def get_llm_logger(self, name="llm_global"):
        """
        logger specifico per monitoraggio interfaccia servizio LLM
        """
        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(self.level)

        rotating_handler = RotatingFileHandler(
            os.path.join(self.llm_log_dir, "llm.log"),
            maxBytes=1000000,
            backupCount=5
        )

        log_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s \n'
        )

        rotating_handler.setFormatter(log_format)
        logger.addHandler(rotating_handler)

        if self.env != "production":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            logger.addHandler(console_handler)

        return logger
