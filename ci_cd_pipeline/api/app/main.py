import os
import pickle
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

from app.models import ReviewRequest, SentimentResponse

MODEL_PATH = os.environ.get("MODEL_PATH", "/app/model/sentiment_analysis_model.pkl")

PREDICT_COUNTER = Counter(
    "predict_requests_total",
    "Total number of predict requests",
    ["status"],
)
PREDICT_LATENCY = Histogram(
    "predict_latency_seconds",
    "Latency of predict requests in seconds",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/predict", response_model=SentimentResponse)
def predict(request: ReviewRequest):
    PREDICT_COUNTER.labels(status="received").inc()
    with PREDICT_LATENCY.time():
        result = model.predict([request.text])[0]
    sentiment = str(result)
    PREDICT_COUNTER.labels(status="success").inc()
    return SentimentResponse(text=request.text, sentiment=sentiment)


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
