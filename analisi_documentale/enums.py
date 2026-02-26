from enum import Enum

class AppEnv(Enum):
    STAGING = "staging"
    PRODUCTION = "production"

class AgentActionType(Enum):
    DIRECT_QUERY = "direct_query"
    REPORT = "report_generation"

class GroqModelId(Enum):
    OSS120 = "openai/gpt-oss-120b"
    LLAMA70 = "llama-3.3-70b-versatile"
