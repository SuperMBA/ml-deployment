import os
import logging

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

# --- logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ml")

app = FastAPI()

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")
model = joblib.load("model.pkl")


class PredictRequest(BaseModel):
    x: list[float]


@app.get("/health")
def health():
    return {"status": "ok", "version": MODEL_VERSION}


@app.post("/predict")
def predict(req: PredictRequest):
    logger.info("predict request x=%s version=%s", req.x, MODEL_VERSION)

    preds = model.predict(np.array(req.x).reshape(-1, 1)).tolist()

    logger.info("predict response preds=%s version=%s", preds, MODEL_VERSION)
    return {"predictions": preds, "model_version": MODEL_VERSION}


@app.on_event("startup")
def _startup():
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
