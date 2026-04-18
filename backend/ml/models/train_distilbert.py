import os
from pathlib import Path

import numpy as np
import pandas as pd
import evaluate
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_recall_fscore_support

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    pipeline,
)
import torch


# -----------------------------
# Paths and labels
# -----------------------------
DATA_PATH = Path("../../data/processed/cleaned_train.csv")
OUTPUT_DIR = Path("../saved/distilbert_model")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LABELS = {0: "mild", 1: "moderate", 2: "severe"}
ID2LABEL = {0: "mild", 1: "moderate", 2: "severe"}
LABEL2ID = {"mild": 0, "moderate": 1, "severe": 2}

MODEL_NAME = "distilbert-base-uncased"
MAX_LENGTH = 128
RANDOM_STATE = 42


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

if "text" not in df.columns or "label" not in df.columns:
    raise ValueError("Dataset must contain 'text' and 'label' columns.")

df["text"] = df["text"].astype(str)
df["label"] = df["label"].astype(int)

print("Dataset shape:", df.shape)
print("\nClass distribution:")
print(df["label"].value_counts().sort_index())

# Stratified split: train / temp, then temp -> val / test
train_df, temp_df = train_test_split(
    df,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=df["label"]
)

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.5,
    random_state=RANDOM_STATE,
    stratify=temp_df["label"]
)

print("\nTrain shape:", train_df.shape)
print("Validation shape:", val_df.shape)
print("Test shape:", test_df.shape)


# -----------------------------
# Convert to Hugging Face Dataset
# -----------------------------
train_ds = Dataset.from_pandas(train_df.reset_index(drop=True))
val_ds = Dataset.from_pandas(val_df.reset_index(drop=True))
test_ds = Dataset.from_pandas(test_df.reset_index(drop=True))


# -----------------------------
# Tokenizer
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=MAX_LENGTH
    )

tokenized_train = train_ds.map(tokenize_function, batched=True)
tokenized_val = val_ds.map(tokenize_function, batched=True)
tokenized_test = test_ds.map(tokenize_function, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


# -----------------------------
# Model
# -----------------------------
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3,
    id2label=ID2LABEL,
    label2id=LABEL2ID
)


# -----------------------------
# Metrics
# -----------------------------
accuracy_metric = evaluate.load("accuracy")
precision_metric = evaluate.load("precision")
recall_metric = evaluate.load("recall")
f1_metric = evaluate.load("f1")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    accuracy = accuracy_score(labels, predictions)
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        labels, predictions, average="macro", zero_division=0
    )
    _, _, f1_weighted, _ = precision_recall_fscore_support(
        labels, predictions, average="weighted", zero_division=0
    )

    return {
        "accuracy": accuracy,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
    }


# -----------------------------
# Training arguments
# -----------------------------
# If you have a GPU, fp16 may help. On CPU, keep fp16=False.
use_fp16 = torch.cuda.is_available()

training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR),
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1_macro",
    greater_is_better=True,
    save_total_limit=2,
    fp16=use_fp16,
    report_to="none",
    seed=RANDOM_STATE
)


# -----------------------------
# Trainer
# -----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    processing_class=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)


# -----------------------------
# Train
# -----------------------------
print("\nStarting DistilBERT training...")
trainer.train()

print("\nSaving best model...")
trainer.save_model(str(OUTPUT_DIR))
tokenizer.save_pretrained(str(OUTPUT_DIR))


# -----------------------------
# Validation metrics
# -----------------------------
print("\nValidation results:")
val_metrics = trainer.evaluate(tokenized_val)
print(val_metrics)


# -----------------------------
# Test metrics
# -----------------------------
print("\nTest results:")
test_metrics = trainer.evaluate(tokenized_test)
print(test_metrics)


# -----------------------------
# Detailed test predictions
# -----------------------------
pred_output = trainer.predict(tokenized_test)
y_true = pred_output.label_ids
y_pred = np.argmax(pred_output.predictions, axis=-1)

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))

print("\nClassification Report:")
print(
    classification_report(
        y_true,
        y_pred,
        target_names=["mild", "moderate", "severe"],
        zero_division=0
    )
)

# Save test predictions
pred_df = test_df.copy()
pred_df["predicted_label"] = y_pred
pred_df["predicted_name"] = pred_df["predicted_label"].map(LABELS)
pred_df["true_name"] = pred_df["label"].map(LABELS)
pred_df.to_csv(OUTPUT_DIR / "test_predictions.csv", index=False)

print(f"\nSaved predictions to: {OUTPUT_DIR / 'test_predictions.csv'}")


# -----------------------------
# Quick manual inference examples
# -----------------------------
device = 0 if torch.cuda.is_available() else -1

clf = pipeline(
    "text-classification",
    model=str(OUTPUT_DIR),
    tokenizer=str(OUTPUT_DIR),
    device=device
)

examples = [
    "mild headache and slight fever",
    "high fever vomiting and dizziness for two days",
    "I have chest pain and difficulty breathing",
    "severe chest pain shortness of breath and fainting",
    "unconscious and not breathing properly"
]

print("\nManual inference examples:")
for text in examples:
    result = clf(text)[0]
    print({"text": text, "prediction": result["label"], "score": round(result["score"], 4)})

summary = {
    "model": "DistilBERT",
    "test_accuracy": float(test_metrics.get("eval_accuracy", 0.0)),
    "test_f1_macro": float(test_metrics.get("eval_f1_macro", 0.0)),
    "test_f1_weighted": float(test_metrics.get("eval_f1_weighted", 0.0)),
    "test_precision_macro": float(test_metrics.get("eval_precision_macro", 0.0)),
    "test_recall_macro": float(test_metrics.get("eval_recall_macro", 0.0)),
}
pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "metrics_summary.csv", index=False)
print(f"Saved summary to: {OUTPUT_DIR / 'metrics_summary.csv'}")