from dataclasses import dataclass
from typing import Optional, Literal

import threading

from app_logger import LoggerHandler
from monitoring.metrics_db_client import m_db_client


@dataclass
class RAGPerformanceMetrics:
    query: str
    total_time: float
    best_item_score: float
    worst_item_score: float
    mean_score: float
    chunks_ids: list[str]

@dataclass
class AgentPerformanceMetrics:
    action_type: Literal['direct_query', 'report_generation']
    query: str
    total_time: float
    llm_time: float
    success: bool
    upload_time: float = Optional[float]


class MetricsCollector:
    """
    Classe per raccolta e storage di tutte le metriche più importanti
    nel corso di un ciclo completo richiesta-risposta
    """
    def __init__(self, agent_metrics: RAGPerformanceMetrics = None, rag_metrics: RAGPerformanceMetrics = None):
        self.db = m_db_client
        self.agent_metrics = agent_metrics
        self.rag_metrics = rag_metrics

        self.mon_logger = LoggerHandler().get_monitoring_logger(__name__)

    def save(self):
        thread = threading.Thread(target=self._write, daemon=True)
        thread.start()
        thread.join()

    def _write(self):
        try:
            m_db_client.save(self.agent_metrics, self.rag_metrics)
        except Exception as e:
            self.mon_logger.error(f"Error saving metrics: {e}")




