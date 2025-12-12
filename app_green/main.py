import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

model = joblib.load("model.pkl")

class PredictRequest(BaseModel):
    x: list[float]

@app.get("/health")
def health():
    return {"status": "ok", "version": MODEL_VERSION, "color": "green"}

@app.post("/predict")
def predict(req: PredictRequest):
    preds = model.predict([[v] for v in req.x])
    return {"predictions": preds.tolist(), "model_version": MODEL_VERSION}
