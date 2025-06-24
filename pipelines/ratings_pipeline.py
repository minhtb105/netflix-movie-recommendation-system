from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from steps.prepare_data import *
import yaml


def process_ratings_pipeline():
    params = yaml.safe_load(open("params.yaml"))["process_ratings"]
    df = pd.read_csv(params['file_path'])
    
    timestamp_col = params['timestamp_col']
    df = clean_df(df=df, datetime_cols=[timestamp_col])
    df = feature_engineer(df=df, 
                        datetime_cols=[timestamp_col], 
                        groupby_cols=['user_id'], 
                        ts_col=timestamp_col, 
                        drop_original=False) 
    
    df = df.drop(columns=[timestamp_col, "prev_ts"])
    
    target_col = params['target_col']
    test_size = params['test_size']
    X_train, X_test, y_train, y_test = divide_df(df, target_col, test_size)
    
    normalize_columns = params['normalize_columns']
    X_train, X_test = normalize_df(X_train, 
                                   X_test, 
                                   method="standard", 
                                   columns=normalize_columns)
   
    output_dir = Path(params['out_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    X_train.to_csv(f"{output_dir}/X_train.csv", index=False)
    X_test.to_csv(f"{output_dir}/X_test.csv",  index=False)
    y_train.to_csv(f"{output_dir}/y_train.csv", index=False)
    y_test.to_csv(f"{output_dir}/y_test.csv",  index=False)
    
if __name__ == "__main__":
    process_ratings_pipeline()