from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import joblib
import traceback

from nlp.preprocess import normalize_text
from nlp.extractor import extract_symptoms, extract_duration
from nlp.rules import detect_negations, detect_danger_terms

try:
    from app.nlp.extractor import extract_severity_words
except ImportError:
    def extract_severity_words(text: str):
        return []


app = FastAPI(title="TIRP Medical Triage API")


class PredictRequest(BaseModel):
    text: str
    age: Optional[int] = None
    gender: Optional[str] = None
    pain_score: Optional[int] = None
    body_part: Optional[str] = None


class PredictResponse(BaseModel):
    cleaned_text: str
    prediction: str
    confidence: Optional[float]
    symptoms: List[str]
    duration: Optional[str]
    severity_words: List[str]
    danger_terms: List[str]
    negations: List[str]
    recommendation: str
    pain_score: Optional[int] = None
    body_part: Optional[str] = None


BASE_DIR = os.path.dirname(__file__)
SAVED_DIR = os.path.join(BASE_DIR, "saved")
MODEL_PATH = os.path.join(SAVED_DIR, "linear_svc.joblib")

model = None


def load_model():
    global model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")


try:
    load_model()
except Exception:
    print("❌ Error loading model:")
    print(traceback.format_exc())


def get_actual_model():
    global model

    if model is None:
        raise RuntimeError("Model not loaded")

    if isinstance(model, dict):
        print("Model is dict. Keys:", list(model.keys()))

        if "linear_svc" in model:
            return model["linear_svc"]

        return list(model.values())[0]

    return model


def map_prediction_label(prediction):
    label_map = {
        0: "mild",
        1: "moderate",
        2: "severe",
        "0": "mild",
        "1": "moderate",
        "2": "severe",
        "mild": "mild",
        "moderate": "moderate",
        "severe": "severe",
    }
    return label_map.get(prediction, str(prediction))


def predict_label(text: str):
    actual_model = get_actual_model()

    raw_prediction = actual_model.predict([text])[0]
    prediction = map_prediction_label(raw_prediction)

    confidence = None
    if hasattr(actual_model, "predict_proba"):
        probs = actual_model.predict_proba([text])[0]
        confidence = float(max(probs))

    return prediction, confidence


def adjust_prediction(prediction: str, pain_score: Optional[int], body_part: Optional[str]) -> str:
    pred = str(prediction).lower()
    part = str(body_part).lower() if body_part else None

    if pain_score is not None and pain_score >= 8 and pred == "mild":
        pred = "moderate"

    if part == "chest" and pain_score is not None and pain_score >= 7:
        pred = "severe"

    if part == "head" and pain_score is not None and pain_score >= 9:
        pred = "severe"

    if part in ["abdomen", "back"] and pain_score is not None and pain_score >= 8 and pred == "mild":
        pred = "moderate"

    return pred


def generate_recommendation(prediction: str, danger_terms: List[str], pain_score: Optional[int], body_part: Optional[str]) -> str:
    p = str(prediction).lower()
    part = str(body_part).lower() if body_part else None

    if danger_terms:
        return "Urgent warning signs detected. Seek immediate medical attention."

    if part == "chest" and pain_score is not None and pain_score >= 7:
        return "Chest pain with a high pain score detected. Seek urgent medical attention immediately."

    if part == "head" and pain_score is not None and pain_score >= 9:
        return "Severe head pain detected. Seek urgent medical attention immediately."

    if p == "mild":
        return "Symptoms appear mild. Monitor closely and seek routine care if needed."
    elif p == "moderate":
        return "Medical review is recommended soon."
    elif p == "severe":
        return "Seek urgent medical attention immediately."

    return "No recommendation available."


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
    }


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    try:
        print("\n🔹 NEW REQUEST 🔹")

        raw_text = payload.text or ""
        cleaned = normalize_text(raw_text)
        print("Cleaned:", cleaned)

        symptoms = extract_symptoms(cleaned)
        symptoms = list(symptoms) if symptoms else []
        print("Symptoms:", symptoms)

        duration_raw = extract_duration(cleaned)
        if isinstance(duration_raw, list):
            duration = ", ".join(str(x) for x in duration_raw) if duration_raw else None
        elif duration_raw is None:
            duration = None
        else:
            duration = str(duration_raw)
        print("Duration:", duration)

        severity_words = extract_severity_words(cleaned)
        severity_words = list(severity_words) if severity_words else []
        print("Severity words:", severity_words)

        danger_terms = detect_danger_terms(cleaned)
        danger_terms = list(danger_terms) if danger_terms else []
        print("Danger terms:", danger_terms)

        negations = detect_negations(cleaned)
        negations = list(negations) if negations else []
        print("Negations:", negations)

        if cleaned.strip():
            prediction, confidence = predict_label(cleaned)
        else:
            prediction, confidence = "mild", None

        prediction = adjust_prediction(
            prediction=prediction,
            pain_score=payload.pain_score,
            body_part=payload.body_part,
        )
        print("Prediction:", prediction)

        recommendation = generate_recommendation(
            prediction=prediction,
            danger_terms=danger_terms,
            pain_score=payload.pain_score,
            body_part=payload.body_part,
        )

        return {
            "cleaned_text": str(cleaned),
            "prediction": str(prediction),
            "confidence": float(confidence) if confidence is not None else None,
            "symptoms": symptoms,
            "duration": duration,
            "severity_words": severity_words,
            "danger_terms": danger_terms,
            "negations": negations,
            "recommendation": str(recommendation),
            "pain_score": int(payload.pain_score) if payload.pain_score is not None else None,
            "body_part": str(payload.body_part) if payload.body_part is not None else None,
        }

    except Exception as e:
        print("\n❌ ERROR OCCURRED ❌")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))