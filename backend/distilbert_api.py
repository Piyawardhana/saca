from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from pathlib import Path
import torch

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "saved" / "distilbert_model"

device = 0 if torch.cuda.is_available() else -1

classifier = pipeline(
    "text-classification",
    model=str(MODEL_PATH),
    tokenizer=str(MODEL_PATH),
    device=device
)

class SymptomRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "DistilBERT Triage API is running"}

@app.post("/predict")
def predict(request: SymptomRequest):
    result = classifier(request.text)[0]

    return {
        "input": request.text,
        "predicted_label": result["label"],
        "confidence": round(float(result["score"]), 4)
    }