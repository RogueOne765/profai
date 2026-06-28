from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Review text to analyze")


class SentimentResponse(BaseModel):
    text: str
    sentiment: str
