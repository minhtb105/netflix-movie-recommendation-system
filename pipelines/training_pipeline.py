import pandas as pd
from steps.train_model import train_model
from steps.evaluation import evaluate_model
from src.model_dev import *
from mlflow.tracking import MlflowClient
from steps.fetch_features import (
    get_user_features_df,
    get_movie_features_df,
    get_rating_features_df,
)


def top_n_rating_pipeline():
    df = get_rating_features_df()
    model = PopularityBased()
    model_class = model.__class__
    model_name = model_class.__name__
    get_or_train(model_class, df)

def user_based_cf_pipeline(target_user_id: int):
    df = get_rating_features_df()
    model = UserBasedCF()
    model_class = model.__class__
    model_name = model_class.__name__
    
    get_or_train(model_class, df, target_user_id=target_user_id)

def item_based_cf_pipeline():
    df = get_rating_features_df()
    model = ItemBasedCF()
    model_class = model.__class__
    model_name = model_class.__name__
    get_or_train(model_class)