import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import accuracy_score, f1_score, classification_report


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
SAVE_DIR = os.path.join(BASE_DIR, "ml", "saved", "disease")
RESULTS_DIR = os.path.join(BASE_DIR, "ml", "results", "disease")

FULL_DATASET_PATH = os.path.join(DATA_DIR, "saca_synthetic_patient_cases_30000.csv")

TRAIN_PATH = os.path.join(DATA_DIR, "saca_train.csv")
VALIDATION_PATH = os.path.join(DATA_DIR, "saca_validation.csv")
TEST_PATH = os.path.join(DATA_DIR, "saca_test.csv")

TEXT_COL = "user_text"
TARGET_COL = "primary_disease"

CATEGORICAL_COLS = [
    "age_group",
    "sex",
    "body_part",
    "red_flags_present"
]

NUMERIC_COLS = [
    "duration_days",
    "pain_score",
    "symptom_count"
]

FEATURE_COLS = [TEXT_COL] + CATEGORICAL_COLS + NUMERIC_COLS


def ensure_dirs():
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)


def clean_dataframe(df):
    required_cols = FEATURE_COLS + [TARGET_COL]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Dataset is missing required column: {col}")

    df = df[required_cols].copy()

    df = df.dropna(subset=[TEXT_COL, TARGET_COL])

    df[TEXT_COL] = df[TEXT_COL].astype(str).str.lower().str.strip()
    df[TARGET_COL] = df[TARGET_COL].astype(str).str.lower().str.strip()

    for col in CATEGORICAL_COLS:
        df[col] = df[col].fillna("unknown").astype(str).str.lower().str.strip()

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    return df


def create_train_validation_test_split(
    test_size=0.15,
    validation_size=0.15,
    random_state=42,
    save_splits=True
):
    """
    Reads one full dataset and creates:
    - train set
    - validation set
    - test set

    Default:
    train = 70%
    validation = 15%
    test = 15%
    """

    if not os.path.exists(FULL_DATASET_PATH):
        raise FileNotFoundError(
            f"Full dataset not found:\n{FULL_DATASET_PATH}\n\n"
            "Put your single dataset CSV in backend/data/processed/ "
            "or update FULL_DATASET_PATH."
        )

    df = pd.read_csv(FULL_DATASET_PATH)
    df = clean_dataframe(df)

    print("Full dataset rows after cleaning:", len(df))
    print("Unique disease labels:", df[TARGET_COL].nunique())

    # First split: separate test set
    train_val_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[TARGET_COL]
    )

    # Second split: validation from remaining train_val
    # validation_size is relative to full dataset, so convert it relative to train_val
    validation_relative_size = validation_size / (1 - test_size)

    train_df, val_df = train_test_split(
        train_val_df,
        test_size=validation_relative_size,
        random_state=random_state,
        stratify=train_val_df[TARGET_COL]
    )

    train_df = train_df.reset_index(drop=True)
    val_df = val_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    print("\nSplit sizes:")
    print("Train:", len(train_df))
    print("Validation:", len(val_df))
    print("Test:", len(test_df))

    print("\nDisease count check:")
    print("Train diseases:", train_df[TARGET_COL].nunique())
    print("Validation diseases:", val_df[TARGET_COL].nunique())
    print("Test diseases:", test_df[TARGET_COL].nunique())

    if save_splits:
        train_df.to_csv(TRAIN_PATH, index=False)
        val_df.to_csv(VALIDATION_PATH, index=False)
        test_df.to_csv(TEST_PATH, index=False)

        print("\nSaved split files:")
        print(TRAIN_PATH)
        print(VALIDATION_PATH)
        print(TEST_PATH)

    return train_df, val_df, test_df


def load_split_data(force_resplit=False):
    """
    If split files already exist, load them.
    Otherwise, create splits from one full dataset.
    """

    ensure_dirs()

    split_files_exist = (
        os.path.exists(TRAIN_PATH)
        and os.path.exists(VALIDATION_PATH)
        and os.path.exists(TEST_PATH)
    )

    if split_files_exist and not force_resplit:
        print("Loading existing train/validation/test split files...")

        train_df = pd.read_csv(TRAIN_PATH)
        val_df = pd.read_csv(VALIDATION_PATH)
        test_df = pd.read_csv(TEST_PATH)

        train_df = clean_dataframe(train_df)
        val_df = clean_dataframe(val_df)
        test_df = clean_dataframe(test_df)

        return train_df, val_df, test_df

    print("Creating train/validation/test splits from full dataset...")

    return create_train_validation_test_split(
        test_size=0.15,
        validation_size=0.15,
        random_state=42,
        save_splits=True
    )


def build_preprocessor(max_features=20000):
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "text",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 3),
                    max_features=max_features,
                    sublinear_tf=True
                ),
                TEXT_COL
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLS
            ),
            (
                "numeric",
                MinMaxScaler(),
                NUMERIC_COLS
            )
        ]
    )

    return preprocessor


def top_k_accuracy(model, X, y_true, k=3):
    """
    Calculates whether the true disease is inside the top-k predictions.
    Works with models that support predict_proba().
    """

    if not hasattr(model, "predict_proba"):
        raise ValueError("Model does not support predict_proba().")

    probabilities = model.predict_proba(X)
    classes = model.classes_

    top_k_indices = np.argsort(probabilities, axis=1)[:, -k:]

    correct = 0
    y_true = list(y_true)

    for i, true_label in enumerate(y_true):
        top_labels = classes[top_k_indices[i]]
        if true_label in top_labels:
            correct += 1

    return correct / len(y_true)


def evaluate_model(model, X, y, model_name, split_name):
    y_pred = model.predict(X)

    accuracy = accuracy_score(y, y_pred)
    weighted_f1 = f1_score(y, y_pred, average="weighted")
    top3_accuracy = top_k_accuracy(model, X, y, k=3)

    report = classification_report(y, y_pred, zero_division=0)

    print(f"\n{model_name} Results on {split_name}")
    print("Accuracy:", round(accuracy, 4))
    print("Weighted F1:", round(weighted_f1, 4))
    print("Top-3 Accuracy:", round(top3_accuracy, 4))
    print(report)

    return {
        "model_name": model_name,
        "split": split_name,
        "accuracy": accuracy,
        "weighted_f1": weighted_f1,
        "top3_accuracy": top3_accuracy,
        "classification_report": report
    }


def save_report(result, report_path):
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"{result['model_name']} Disease Model\n")
        f.write(f"Split: {result['split']}\n")
        f.write(f"Accuracy: {result['accuracy']:.4f}\n")
        f.write(f"Weighted F1: {result['weighted_f1']:.4f}\n")
        f.write(f"Top-3 Accuracy: {result['top3_accuracy']:.4f}\n\n")
        f.write(result["classification_report"])


def save_model(model, model_path):
    joblib.dump(model, model_path)
    print("Saved model:", model_path)