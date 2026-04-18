import re
import pandas as pd
from pathlib import Path

RAW_PATH = Path("raw/mergedData.csv")
PROCESSED_PATH = Path("processed/cleaned_train.csv")


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    df = pd.read_csv(RAW_PATH, sep=None, engine="python")

    # Select only needed columns
    df = df[["input", "urgency_label"]].copy()
    df.columns = ["text", "label"]

    # Clean text
    df["text"] = df["text"].apply(clean_text)

    # Remove empty rows
    df = df[df["text"] != ""]

    # Ensure labels are integers
    df["label"] = df["label"].astype(int)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print("Preprocessing complete.")
    print(df.head())

    print("\nClass distribution:")
    print(df["label"].value_counts())


if __name__ == "__main__":
    main()