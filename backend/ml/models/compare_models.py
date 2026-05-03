import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from label_config import REVERSE_LABEL_MAP


BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent.parent

DATA_PATH = BACKEND_DIR / "data" / "processed" / "cleaned_train1.csv"
SAVE_DIR = BACKEND_DIR / "ml" / "saved"
PLOT_DIR = BACKEND_DIR / "ml" / "results"

SAVE_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)


def build_models():
    return {
        "Logistic Regression": Pipeline([
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
        ]),

        "Linear SVC": Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=20000,
                min_df=2,
                max_df=0.9,
                sublinear_tf=True
            )),
            ("clf", LinearSVC(
                class_weight="balanced",
                random_state=42
            ))
        ]),

        "Naive Bayes": Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=20000,
                min_df=2,
                max_df=0.9,
                sublinear_tf=True
            )),
            ("clf", MultinomialNB(alpha=1.0))
        ])
    }


def main():
    df = pd.read_csv(DATA_PATH)

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV must contain 'text' and 'label' columns.")

    df = df.dropna(subset=["text", "label"])

    X = df["text"].astype(str)
    y = df["label"]

    labels = sorted(y.unique())
    target_names = [REVERSE_LABEL_MAP[i] for i in labels]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    models = build_models()
    results = []

    best_model = None
    best_name = None
    best_score = -1

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test,
            y_pred,
            average="weighted",
            zero_division=0
        )

        macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
            y_test,
            y_pred,
            average="macro",
            zero_division=0
        )

        results.append({
            "Model": name,
            "Accuracy": accuracy,
            "Weighted Precision": precision,
            "Weighted Recall": recall,
            "Weighted F1": f1,
            "Macro Precision": macro_precision,
            "Macro Recall": macro_recall,
            "Macro F1": macro_f1
        })

        print("\nClassification Report:")
        print(classification_report(
            y_test,
            y_pred,
            labels=labels,
            target_names=target_names,
            zero_division=0
        ))

        cm = confusion_matrix(y_test, y_pred, labels=labels)
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=target_names
        )

        disp.plot(cmap="Blues", values_format="d")
        plt.title(f"Confusion Matrix - {name}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(PLOT_DIR / f"{name.lower().replace(' ', '_')}_confusion_matrix.png")
        plt.close()

        # Choose best model using Macro F1, not just accuracy.
        # Macro F1 is better for imbalanced triage classes.
        if macro_f1 > best_score:
            best_score = macro_f1
            best_model = model
            best_name = name

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="Macro F1", ascending=False)

    print("\nFinal Model Comparison:")
    print(results_df)

    results_df.to_csv(PLOT_DIR / "model_comparison_results.csv", index=False)

    # Accuracy comparison
    plt.figure(figsize=(9, 5))
    plt.bar(results_df["Model"], results_df["Accuracy"])
    plt.title("Model Accuracy Comparison")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "accuracy_comparison.png")
    plt.close()

    # Macro F1 comparison
    plt.figure(figsize=(9, 5))
    plt.bar(results_df["Model"], results_df["Macro F1"])
    plt.title("Model Macro F1 Comparison")
    plt.ylabel("Macro F1 Score")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "macro_f1_comparison.png")
    plt.close()

    # Weighted F1 comparison
    plt.figure(figsize=(9, 5))
    plt.bar(results_df["Model"], results_df["Weighted F1"])
    plt.title("Model Weighted F1 Comparison")
    plt.ylabel("Weighted F1 Score")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "weighted_f1_comparison.png")
    plt.close()

    print(f"\nBest model based on Macro F1: {best_name}")
    print(f"Best Macro F1 Score: {best_score:.4f}")
    print(f"\nGraphs saved in: {PLOT_DIR.resolve()}")


if __name__ == "__main__":
    main()