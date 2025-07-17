from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from steps.prepare_data import clean_df, vectorize_text
from src.feature_engineer import FeatureEngineer
import pandas as pd
import yaml

def process_movies_pipeline():
    params = yaml.safe_load(open("params.yaml"))["process_movies"]
    df = pd.read_csv(params['file_path'])
    
    date_col = params['date_col']
    df = clean_df(df, datetime_cols=[date_col])
    
    df = FeatureEngineer.add_time_features(
        df,
        datetime_cols=[date_col],
        drop_original=False
    )
    
    vectorize_col = params['vectorize_col']
    max_features = params['max_features']
    df, _ = vectorize_text(df_train=df,
                            column=vectorize_col,
                            max_features=max_features) 
    
    # Drop original dates
    df = df.drop(columns=['IMDb_URL'])
    
    output_dir = Path(params['out_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(f"{output_dir}/movie_features_train.parquet", index=False)

if __name__ == "__main__":
    process_movies_pipeline()