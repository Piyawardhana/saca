import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import LinearSVC

from label_config import REVERSE_LABEL_MAP

DATA_PATH = Path("../../data/processed/cleaned_train1.csv")
SAVE_DIR = Path("../saved")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def build_models():
    model = {
        "linear_svc": Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=20000,
                min_df=2,
                max_df=0.9,
                sublinear_tf=True
                )),
            ("clf", LinearSVC(class_weight="balanced", random_state=42))
        ])
    }
    return model


def main():
    df = pd.read_csv(DATA_PATH)

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = build_models()
    results = []

    best_model = None
    best_name = None
    best_accuracy = 0

    for name, pipeline in model.items():
        print(f"\nTraining: {name}")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        results.append((name, acc))

        print(f"Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(
            y_test,
            y_pred,
            target_names=[REVERSE_LABEL_MAP[i] for i in sorted(REVERSE_LABEL_MAP.keys())]
        ))

        model_path = SAVE_DIR / f"{name}.joblib"
        joblib.dump(pipeline, model_path)

    if model is not None:
        model_path = SAVE_DIR / "linear_svc.joblib"
        joblib.dump(model, model_path)

        metadata = {
            "best_model_name": best_name,
            "best_accuracy": best_accuracy
        }
        joblib.dump(metadata, SAVE_DIR / "model_metadata.joblib")


if __name__ == "__main__":
    main()