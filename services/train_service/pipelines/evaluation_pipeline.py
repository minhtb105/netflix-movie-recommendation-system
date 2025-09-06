from pathlib import Path
import sys
import mlflow
from steps.evaluate import evaluate_model


def evaluation_pipeline(model, X_test, y_test, k=10):
    mlflow.set_experiment("ModelEvaluation")

    with mlflow.start_run(run_name="EvaluationPipeline"):
        evaluate_model(model, X_test, y_test, k=k)
        mlflow.set_tag("step", "evaluation_pipeline")
