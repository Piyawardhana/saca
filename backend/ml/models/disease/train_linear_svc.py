import os

from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

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


MODEL_NAME = "Linear SVC"
MODEL_PATH = os.path.join(SAVE_DIR, "disease_linear_svc.joblib")
REPORT_PATH = os.path.join(RESULTS_DIR, "disease_linear_svc_report.txt")


def make_calibrated_linear_svc():
    base_model = LinearSVC(
        C=1.0,
        class_weight="balanced",
        random_state=42,
        max_iter=5000
    )

    try:
        return CalibratedClassifierCV(
            estimator=base_model,
            cv=3
        )
    except TypeError:
        return CalibratedClassifierCV(
            base_estimator=base_model,
            cv=3
        )


def train_linear_svc():
    ensure_dirs()

    train_df, val_df, _ = load_split_data()

    X_train = train_df[FEATURE_COLS]
    y_train = train_df[TARGET_COL]

    X_val = val_df[FEATURE_COLS]
    y_val = val_df[TARGET_COL]

    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(max_features=20000)),
            ("model", make_calibrated_linear_svc())
        ]
    )

    print("\nTraining Linear SVC disease model...")
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
    train_linear_svc()