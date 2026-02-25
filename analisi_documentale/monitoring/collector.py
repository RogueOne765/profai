import threading

from app_logger import LoggerHandler
from monitoring.metrics_db import m_db
from monitoring.models import AgentPerformanceMetrics, RAGPerformanceMetrics


class MetricsCollector:
    """
    Classe per raccolta e storage di tutte le metriche più importanti
    nel corso di un ciclo completo richiesta-risposta
    """
    def __init__(self, agent_metrics: AgentPerformanceMetrics = None, rag_metrics: RAGPerformanceMetrics = None):
        self.db = m_db
        self.agent_metrics = agent_metrics
        self.rag_metrics = rag_metrics

        self.mon_logger = LoggerHandler().get_monitoring_logger(__name__)

    def save(self):
        thread = threading.Thread(target=self._write, daemon=True)
        thread.start()
        thread.join()

    def _write(self):
        try:
            m_db.save(self.agent_metrics, self.rag_metrics)
        except Exception as e:
            self.mon_logger.error(f"Error saving metrics: {e}")




