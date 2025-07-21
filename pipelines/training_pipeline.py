from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
from steps.train_model import get_or_train
from src.model_dev import (
    UserBasedCF, ItemBasedCF, ContentBasedFiltering
    UserCFPyfuncModel, ItemCFPyfuncModel, ContentFPyfuncModel
    compute_user_item_matrix
)
from steps.fetch_features import (
    get_user_features_df,
    get_movie_features_df,
    get_rating_features_df,
)
import warnings
import mlflow


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def save_user_item_matrix():
    mlflow.set_experiment("SaveUserItemMatrix")
     
    with mlflow.start_run(run_name="SaveUserItemMatrix"):
        df = get_rating_features_df()
        mlflow.log_param("num_rows", len(df))
        compute_user_item_matrix(df)
        mlflow.set_tag("step", "create_user_item_matrix")

def user_based_cf_pipeline():
    mlflow.set_experiment("UserBasedCF")
    
    with mlflow.start_run(run_name="UserBasedCFPipeline"):
        base_model = UserBasedCF()
        base_model.train()
        model = UserCFPyfuncModel(model=base_model)
        get_or_train(model)

def item_based_cf_pipeline():
    mlflow.set_experiment("ItemBasedCF")
    
    with mlflow.start_run(run_name="ItemBasedCFPipeline"):
        base_model = ItemBasedCF()
        base_model.train()
        model = ItemCFPyfuncModel(model=base_model)
        get_or_train(model)
    
def content_based_filtering_pipeline():
    mlflow.set_experiment("ContentBasedF")
    
    with mlflow.start_run(run_name="ContentBasedFPipeline"):
        base_model = ContentBasedFiltering()
        base_model.train()
        model = ContentFPyfuncModel(model=base_model)
        get_or_train(model)
    