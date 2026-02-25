from enums import AgentActionType
from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class RAGPerformanceMetrics:
    query: str
    total_time: float
    best_score: float
    worst_score: float
    mean_score: float
    chunks_ids: Optional[str]

@dataclass
class AgentPerformanceMetrics:
    action_type: str
    query: str
    total_time: float
    llm_time: float
    upload_time: float = 0
