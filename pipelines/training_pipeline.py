from zenml import pipeline
from steps.ingest_data import ingest_df
from steps.feature_engineering import feature_df
from steps.clean_data import clean_df
from steps.train_model import train_model
from steps.evaluation import evaluate_model

@pipeline(enable_cache=True)
def train_pipeline(data_path: str):
    df = ingest_df(data_path)
    feature_df(df)
    clean_df(df)
    train_model(df)
    evaluate_model(df)
