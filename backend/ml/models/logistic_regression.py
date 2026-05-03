import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression

from label_config import REVERSE_LABEL_MAP


# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent.parent

DATA_PATH = BACKEND_DIR / "data" / "processed" / "cleaned_train1.csv"
SAVE_DIR = BACKEND_DIR / "ml" / "saved"

SAVE_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Build model
# --------------------------------------------------
def build_model():
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=20000,
            min_df=2,
            max_df=0.9,
            sublinear_tf=True
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ))
    ])

    return model


# --------------------------------------------------
# Main training function
# --------------------------------------------------
def main():
    print("Looking for CSV at:", DATA_PATH.resolve())
    print("File exists:", DATA_PATH.exists())

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH.resolve()}")

    df = pd.read_csv(DATA_PATH)

    print("\nColumns found:", df.columns.tolist())

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV must contain 'text' and 'label' columns.")

    df = df.dropna(subset=["text", "label"])

    X = df["text"].astype(str)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = build_model()

    print("\nTraining: logistic_regression")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=[
            REVERSE_LABEL_MAP[i]
            for i in sorted(REVERSE_LABEL_MAP.keys())
        ]
    ))

    model_path = SAVE_DIR / "logistic_regression.joblib"
    joblib.dump(model, model_path)

    metadata = {
        "best_model_name": "logistic_regression",
        "best_accuracy": accuracy,
        "model_path": str(model_path)
    }

    joblib.dump(metadata, SAVE_DIR / "logistic_regression_metadata.joblib")

    print("\nModel saved to:", model_path.resolve())
    print("Metadata saved to:", (SAVE_DIR / "model_metadata.joblib").resolve())


if __name__ == "__main__":
    main()