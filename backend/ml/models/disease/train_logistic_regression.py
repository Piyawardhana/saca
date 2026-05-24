import os
import joblib

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from disease_common import (
    SAVE_DIR,
    RESULTS_DIR,
    FEATURE_COLS,
    TARGET_COL,
    ensure_dirs,
    load_split_data,
    build_preprocessor,
    evaluate_model,
    save_report,
    save_model
)


MODEL_NAME = "Logistic Regression"
MODEL_PATH = os.path.join(SAVE_DIR, "disease_logistic_regression.joblib")
REPORT_PATH = os.path.join(RESULTS_DIR, "disease_logistic_regression_report.txt")


def train_logistic_regression():
    ensure_dirs()

    train_df, val_df, _ = load_split_data()

    X_train = train_df[FEATURE_COLS]
    y_train = train_df[TARGET_COL]

    X_val = val_df[FEATURE_COLS]
    y_val = val_df[TARGET_COL]

    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(max_features=20000)),
            (
                "model",
                LogisticRegression(
                    max_iter=5000,
                    class_weight="balanced",
                    solver="lbfgs"
                )
            )
        ]
    )

    print("\nTraining Logistic Regression disease model...")
    pipeline.fit(X_train, y_train)

    result = evaluate_model(
        model=pipeline,
        X=X_val,
        y=y_val,
        model_name=MODEL_NAME,
        split_name="validation"
    )

    save_model(pipeline, MODEL_PATH)
    save_report(result, REPORT_PATH)

    result["model_path"] = MODEL_PATH

    return result


if __name__ == "__main__":
    train_logistic_regression()