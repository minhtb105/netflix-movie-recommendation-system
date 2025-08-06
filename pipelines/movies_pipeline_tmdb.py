from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from steps.prepare_data import (
    clean_df, vectorize_text, 
    normalize_df, encode_df,
    multi_label_encode_df,
)
from src.data_strategy import BERTVectorizeStrategy
import pandas as pd
import numpy as np
import yaml
from datetime import datetime, UTC 


def process_movies_pipeline(params: dict = None):
    if params is None:
        params = yaml.safe_load(open("params.yaml"))["process_movies_tmdb"]
        
    df = pd.read_json(params['file_path'])
    
    df["video_key"] = df["videos"].apply(lambda vids: vids[0]["key"] if isinstance(vids, list) and len(vids) > 0 else "unknown")
    
    drop_cols = params['drop_cols']
    df = df.drop(columns=drop_cols)
    
    vectorize_cols = params['vectorize_cols']
    output_cols = params['output_cols']
    for col, output_col in zip(vectorize_cols, output_cols):
        df, _ = vectorize_text(df, column=col, output_col=output_col, strategy=BERTVectorizeStrategy())
        
    normalize_col = params['normalize_col']
    df, _ = normalize_df(df, columns=normalize_col)
    
    log_transform_cols = params['log_transform_cols']
    df, _ = normalize_df(df, log_transform_columns=log_transform_cols)

    enc_cols = params['enc_cols']
    df, _ = encode_df(df_train=df, columns=enc_cols)
    
    multi_lable_enc_cols = params['multi_lable_enc_cols']
    df, _ = multi_label_encode_df(df, columns=multi_lable_enc_cols)
   
    review_df = pd.read_json(params['review_path'])
    review_df, _ = vectorize_text(
        review_df, 
        column='content',
        output_col='content_vectorize',
        strategy=BERTVectorizeStrategy()
    )
   
    keep_cols = params['keep_cols']
    df = combine_features(df, vector_cols=df.columns, keep_cols=keep_cols)
    if "event_timestamp" not in df.columns:
        df["event_timestamp"] = datetime.now(UTC)
        review_df["event_timestamp"] = datetime.now(UTC)
        
    
    output_dir = Path(params['out_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    df.to_parquet(f"{output_dir}/movie_features_{timestamp}.parquet", index=False)
    review_df.to_parquet(f"{output_dir}/movie_reviews_{timestamp}.parquet", index=False)


def combine_features(df: pd.DataFrame, vector_cols: list[str], keep_cols: list[str]) -> pd.DataFrame:
    """
    Combine all feature columns (which are lists/vectors) into a single vector column.
    """
    feature_cols = [col for col in vector_cols if col not in keep_cols]

    def merge_vectors(row):
        vectors = []
        for col in feature_cols:
            value = row[col]
            if value is None:
                raise ValueError(f"Column '{col}' contains None at row {row.name}")

            array = np.array(value)
            if array.ndim == 0:
                array = np.array([value])

            vectors.append(array)

        return np.concatenate(vectors)

    df['feature_vector'] = df.apply(merge_vectors, axis=1)
    df = df.drop(columns=feature_cols)
    
    return df


if __name__ == "__main__":
    process_movies_pipeline()