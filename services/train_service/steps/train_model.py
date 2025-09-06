import mlflow
import mlflow.pyfunc as pyfunc
from mlflow.tracking import MlflowClient
from mlflow.pyfunc import PythonModel
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def train_model(py_model: PythonModel, run_name: str) -> None:
    class_name = py_model.__class__.__name__
    mlflow.log_param("model_type", class_name)
        
    py_model.model.train()
        
    input_example = [{"user_id": 1, "item_id": 1, "k": 5}]
          
    pyfunc.log_model(
        artifact_path="model",
        python_model=py_model,
        registered_model_name=f"{class_name}_model",
        input_example=input_example,
    )
        
        
def get_or_train(model_instance: PythonModel) -> PythonModel:
    client = MlflowClient()
    model_class = model_instance.__class__
    model_name = model_class.__name__
    
    experiment = client.get_experiment_by_name(model_name)
    if experiment is None:
        experiment_id = client.create_experiment(model_name)
    else:
        experiment_id = experiment.experiment_id

    runs = client.search_runs(
        experiment_ids=[experiment_id],
        filter_string=f"tags.mlflow.runName = '{model_name}'",
        order_by=["start_time desc"],
        max_results=1
    )
    if runs:
        return mlflow.pyfunc.load_model(f"runs:/{runs[0].info.run_id}/model")

    train_model(model_instance, run_name=model_name)
    
    return model_instance