from pathlib import Path
import yaml
import sys
from steps.prepare_data import *


service_root = Path(__file__).resolve().parent.parent
if str(service_root) not in sys.path:
    sys.path.insert(0, str(service_root))

def process_ratings_pipeline():
    params = yaml.safe_load(open(service_root / "params.yaml"))["process_ratings_movielens"]
    df = pd.read_csv(params['file_path'])
    
    timestamp_col = params['timestamp_col']
    df = clean_df(df=df, datetime_cols=[timestamp_col])
    df = feature_engineer(df=df, 
                        datetime_cols=[timestamp_col], 
                        groupby_cols=['user_id'], 
                        ts_col=timestamp_col, 
                        drop_original=False) 
    
    df = df.drop(columns=["prev_ts"])
    
    test_size = params['test_size']
    df_train, df_test = divide_df(df, test_size)
   
    output_dir = Path(params['out_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    df_train.to_parquet(f"{output_dir}/rating_train.parquet", index=False)
    df_test.to_parquet(f"{output_dir}/rating_test.parquet",  index=False)
    
if __name__ == "__main__":
    process_ratings_pipeline()