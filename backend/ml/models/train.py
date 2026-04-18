import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

from label_config import REVERSE_LABEL_MAP

DATA_PATH = Path("../../data/processed/cleaned_train.csv")
SAVE_DIR = Path("../saved")
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def build_models():
    models = {
        "logistic_regression": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
            ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))
        ]),
        "naive_bayes": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
            ("clf", MultinomialNB())
        ]),
        "linear_svc": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
            ("clf", LinearSVC(class_weight="balanced", random_state=42))
        ]),
        "random_forest": Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
            ("clf", RandomForestClassifier(n_estimators=200, random_state=42))
        ]),
    }
    return models


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

    models = build_models()
    results = []

    best_model = None
    best_name = None
    best_accuracy = 0

    for name, pipeline in models.items():
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

        if acc > best_accuracy:
            best_accuracy = acc
            best_model = pipeline
            best_name = name

    print("\n=== Final Comparison ===")
    for name, acc in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"{name}: {acc:.4f}")

    if best_model is not None:
        best_model_path = SAVE_DIR / "best_model.joblib"
        joblib.dump(best_model, best_model_path)

        metadata = {
            "best_model_name": best_name,
            "best_accuracy": best_accuracy
        }
        joblib.dump(metadata, SAVE_DIR / "model_metadata.joblib")

        print(f"\nBest model: {best_name}")
        print(f"Best accuracy: {best_accuracy:.4f}")
        print(f"Saved to: {best_model_path}")


if __name__ == "__main__":
    main()