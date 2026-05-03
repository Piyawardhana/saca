import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import MultinomialNB

from label_config import REVERSE_LABEL_MAP


BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent.parent

DATA_PATH = BACKEND_DIR / "data" / "processed" / "cleaned_train1.csv"
SAVE_DIR = BACKEND_DIR / "ml" / "saved"

SAVE_DIR.mkdir(parents=True, exist_ok=True)


def build_model():
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=20000,
            min_df=2,
            max_df=0.9,
            sublinear_tf=True
        )),
        ("clf", MultinomialNB(
            alpha=1.0
        ))
    ])

    return model


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

    print("\nTraining: naive_bayes")
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
        ],
        zero_division=0
    ))

    model_path = SAVE_DIR / "naive_bayes.joblib"
    joblib.dump(model, model_path)

    metadata = {
        "best_model_name": "naive_bayes",
        "best_accuracy": accuracy,
        "model_path": str(model_path)
    }

    joblib.dump(metadata, SAVE_DIR / "naive_bayes_metadata.joblib")

    print("\nModel saved to:", model_path.resolve())
    print("Metadata saved to:", (SAVE_DIR / "naive_bayes_metadata.joblib").resolve())


if __name__ == "__main__":
    main()