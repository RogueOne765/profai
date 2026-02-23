import sqlite3
from contextlib import contextmanager

from app_logger import LoggerHandler
from monitoring.collector import AgentPerformanceMetrics, RAGPerformanceMetrics


class MetricsDBClient:

    def __init__(self, db_path="metrics.db"):
        self.db_path = db_path
        self._init_db()

        self.mon_logger = LoggerHandler().get_monitoring_logger(__name__)

        self.mon_logger.info(f"Initializing {__name__}...")
        self._init_db()

    def _init_db(self):
        """
        Per fini demo crea tabelle con metodo e non con script migrazione
        """
        self.mon_logger.info(f"Creating monitoring db tables...")
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS requests (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp           DATETIME DEFAULT CURRENT_TIMESTAMP,
                    query               TEXT NOT NULL,
                    action_type         TEXT,
                    total_time          INTEGER,
                    llm_time            INTEGER,
                    upload_time         INTEGER,
                    success             BOOLEAN,
                );
                
                CREATE TABLE IF NOT EXISTS rag_retrieves (
                    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id          INTEGER FOREIGN KEY,
                    timestamp           DATETIME DEFAULT CURRENT_TIMESTAMP,
                    query               TEXT NOT NULL,
                    total_time          INTEGER,
                    best_item_score     FLOAT,
                    worst_item_score    FLOAT,
                    mean_score          FLOAT,
                    chunks_ids          TEXT,
                );
            """)

    @contextmanager
    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def save(self, agent_metrics: AgentPerformanceMetrics, rag_metrics: RAGPerformanceMetrics):
        if not isinstance(agent_metrics, AgentPerformanceMetrics):
            self.mon_logger.error(f"agent_metrics must be of type AgentPerformanceMetrics: {agent_metrics}")
            raise ValueError("agent_metrics must be of type AgentPerformanceMetrics")
        if rag_metrics and not isinstance(rag_metrics, RAGPerformanceMetrics):
            self.mon_logger.error(f"agent_metrics must be of type AgentPerformanceMetrics: {rag_metrics}")
            raise ValueError("rag_metrics must be of type RAGPerformanceMetrics")

        try:
            self.mon_logger.debug(f"Start saving new request on monitoring db: {agent_metrics}")
            with self._get_conn() as conn:
                cursor = conn.execute(
                    """INSERT INTO requests (query, action_type, total_time, llm_time, upload_time, success)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (agent_metrics.query, agent_metrics.action_type, agent_metrics.total_time, agent_metrics.llm_time, agent_metrics.upload_time, agent_metrics.success)
                )

                request_id = cursor.lastrowid

                self.mon_logger.debug(f"New request inserted: {request_id}")

                if rag_metrics:
                    self.mon_logger.debug(f"Start saving new rag stat on monitoring db: {rag_metrics}")
                    rag_cursor = conn.execute(
                        """INSERT INTO rag_retrieves (request_id, query, total_time, best_item_score, worst_item_score, mean_score, chunks_ids)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (request_id, rag_metrics.query, rag_metrics.total_time, rag_metrics.best_item_score, rag_metrics.worst_item_score, rag_metrics.mean_score, rag_metrics.chunks_ids)
                    )
                    self.mon_logger.debug(f"New rag stat succesfully saved: {rag_cursor.lastrowid}")

        except Exception as e:
            self.mon_logger.error(f"Failed saving to metrics db. Error: {e} \n\n agent_metrics: {agent_metrics} \n\n rag_metrics: {rag_metrics}")
            raise Exception(f"Failed saving to metrics db: {e}")

m_db_client = MetricsDBClient()
