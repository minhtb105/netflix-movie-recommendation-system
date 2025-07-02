import logging
from src.model_dev import Model
import mlflow
import mlflow.pyfunc as pyfunc

def train_model(model: Model, df_train: pd.DataFrame, run_name: str, **kwargs) -> None:
    with mlflow.start_run(run_name=run_name):
        model.train(df_train, **kwargs)
        mlflow.log_param("model_type", model.__class__.__name__)
        pyfunc.log_model(
            artifact_path="model",
            python_model=model,
            registered_model_name=f"{model.__class__.__name__}_model"
        )
        
def get_or_train(model_class, df_train: pd.DataFrame, **kwargs):
    client = MlflowClient()
    model_name = model_class.__name__
    experiment = client.get_experiment_by_name(model_name)
    if experiment:
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string=f"tags.mlflow.runName = '{model_name}'",
            order_by=["start_time desc"],
            max_results=1
        )
        if runs:
            return mlflow.pyfunc.load_model(f"runs:/{runs[0].info.run_id}/model")
    model = model_class()
    train_model(model, df_train, run_name=model_name, **kwargs)
    
    return model