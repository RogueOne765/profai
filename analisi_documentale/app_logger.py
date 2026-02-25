import os
import logging
from logging.handlers import RotatingFileHandler
from enums import AppEnv
from dotenv import load_dotenv

class LoggerHandler:
    """
    Gestione logging handler con singleton per utilizzo tra le varie classi dell'applicazione
    """

    def __init__(self):
        """
        Livelli di profondità dei log sono definiti tramite variabile ambiente
        per distinguere staging/produzione
        """
        load_dotenv()
        env = os.getenv("APP_ENV")

        if not env:
            raise ValueError("APP_ENV non impostata")

        try:
            self.app_env = AppEnv(env)
        except ValueError:
            raise ValueError("APP_ENV value not valid")

        self.log_levels = {
            AppEnv.STAGING: logging.DEBUG,
            AppEnv.PRODUCTION: logging.WARNING,
        }

        self.level = self.log_levels[self.app_env] if self.app_env else logging.DEBUG

        """
        Definisce e Crea directory destinazione file di log
        """

        self.base_dir = os.getcwd()
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

        if self.app_env != AppEnv.PRODUCTION:
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

        if self.app_env != AppEnv.PRODUCTION:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_format)
            logger.addHandler(console_handler)

        return logger


    def get_monitoring_logger(self, name="llm_global"):
        """
        logger specifico per operazioni di monitoraggio applicazione
        """
        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(self.level)

        rotating_handler = RotatingFileHandler(
            os.path.join(self.llm_log_dir, "monitoring.log"),
            maxBytes=1000000,
            backupCount=5
        )

        log_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s \n'
        )

        rotating_handler.setFormatter(log_format)
        logger.addHandler(rotating_handler)

        return logger


logger_instance = LoggerHandler()
