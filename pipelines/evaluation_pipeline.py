from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from steps.evaluate import evaluate_model
import mlflow


def evaluation_pipeline(model, X_test, y_test, k=10):
    mlflow.set_experiment("ModelEvaluation")

    with mlflow.start_run(run_name="EvaluationPipeline"):
        evaluate_model(model, X_test, y_test, k=k)
        mlflow.set_tag("step", "evaluation_pipeline")
