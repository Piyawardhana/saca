import os
import shutil
import joblib
import pandas as pd

from disease_common import (
    SAVE_DIR,
    RESULTS_DIR,
    FEATURE_COLS,
    TARGET_COL,
    ensure_dirs,
    load_split_data,
    evaluate_model,
    save_report
)

from train_logistic_regression import train_logistic_regression
from train_linear_svc import train_linear_svc
from train_naive_bayes import train_naive_bayes


FINAL_MODEL_PATH = os.path.join(SAVE_DIR, "disease_model.joblib")
COMPARISON_PATH = os.path.join(RESULTS_DIR, "disease_model_comparison.csv")
FINAL_REPORT_PATH = os.path.join(RESULTS_DIR, "final_disease_model_test_report.txt")


def main():
    ensure_dirs()

    print("\n==============================")
    print("DISEASE IDENTIFICATION MODELS")
    print("==============================\n")

    results = []

    results.append(train_logistic_regression())
    results.append(train_linear_svc())
    results.append(train_naive_bayes())

    summary = pd.DataFrame([
        {
            "Model": r["model_name"],
            "Validation_Accuracy": round(r["accuracy"], 4),
            "Validation_Weighted_F1": round(r["weighted_f1"], 4),
            "Validation_Top3_Accuracy": round(r["top3_accuracy"], 4),
            "Model_Path": r["model_path"]
        }
        for r in results
    ])

    summary = summary.sort_values(
        by=["Validation_Top3_Accuracy", "Validation_Weighted_F1"],
        ascending=False
    )

    print("\n===== VALIDATION COMPARISON =====")
    print(summary)

    summary.to_csv(COMPARISON_PATH, index=False)

    best = max(
        results,
        key=lambda r: (r["top3_accuracy"], r["weighted_f1"])
    )

    print("\nBest disease model selected:")
    print(best["model_name"])
    print("Validation Top-3 Accuracy:", round(best["top3_accuracy"], 4))
    print("Validation Weighted F1:", round(best["weighted_f1"], 4))

    shutil.copy(best["model_path"], FINAL_MODEL_PATH)

    print("\nSaved final selected disease model:")
    print(FINAL_MODEL_PATH)

    # Evaluate selected model on test set
    _, _, test_df = load_split_data()

    X_test = test_df[FEATURE_COLS]
    y_test = test_df[TARGET_COL]

    final_model = joblib.load(FINAL_MODEL_PATH)

    test_result = evaluate_model(
        model=final_model,
        X=X_test,
        y=y_test,
        model_name=best["model_name"],
        split_name="test"
    )

    save_report(test_result, FINAL_REPORT_PATH)

    print("\nSaved comparison CSV:")
    print(COMPARISON_PATH)

    print("\nSaved final test report:")
    print(FINAL_REPORT_PATH)


if __name__ == "__main__":
    main()