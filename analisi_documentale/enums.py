from enum import Enum

class AppEnv(Enum):
    STAGING = "staging"
    PRODUCTION = "production"

class AgentActionType(Enum):
    DIRECT_QUERY = "direct_query"
    REPORT = "report_generation"
