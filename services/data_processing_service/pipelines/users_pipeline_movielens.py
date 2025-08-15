from pathlib import Path
import sys

service_root = Path(__file__).resolve().parent.parent
if str(service_root) not in sys.path:
    sys.path.insert(0, str(service_root))

from typing import List
import pandas as pd
from steps.prepare_data import clean_df, encode_df, normalize_df
import yaml
from datetime import datetime, UTC

def process_users_pipeline():
    params = yaml.safe_load(open(service_root / "params.yaml"))["process_users_movielens"]
    df = pd.read_csv(params['file_path'])
    df = clean_df(df)
    
    enc_cols = params["enc_cols"]
    df, _ = encode_df(df, method="onehot", columns=enc_cols)
    df["event_timestamp"] = datetime.now(UTC)  # event_timestamp_column for feast FileSource
    
    output_dir = Path(params['out_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(f"{output_dir}/user_features.parquet", index=False)
    
if __name__ == "__main__":
    process_users_pipeline()