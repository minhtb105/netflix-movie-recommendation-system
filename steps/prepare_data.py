import pandas as pd
import logging
from typing import List, Tuple, Union, Optional
from src.data_strategy import (
    DataPreprocessStrategy,
    DataDivideStrategy,
    DataEncodeStrategy,
    DataNormalizeStrategy,
    TextVectorizeStrategy,
    DataCleaning,
)
from src.feature_engineer import FeatureEngineer


def clean_df(df: pd.DataFrame, datetime_cols: Optional[List[str]] = None) -> pd.DataFrame:
    # Data cleaning
    preprocess_strategy = DataPreprocessStrategy()
    cleaned_df = preprocess_strategy.handle_data(df, datetime_cols)
    logging.info("Preprocessing completed!")

    return cleaned_df
 
def feature_engineer(df: pd.DataFrame,
                    datetime_cols: Optional[List[str]] = None,
                    groupby_cols: Optional[List[str]] = None,
                    ts_col: str = "timestamp",
                    drop_original: bool = False) -> pd.DataFrame:
    # Feature engineering
    df = FeatureEngineer.add_time_features(df, datetime_cols, drop_original)
    df = FeatureEngineer.add_interaction_gap(df, groupby_cols, ts_col)
    logging.info("Feature engineering added time features and interaction gaps")
    
    return df

def divide_df(df: pd.DataFrame, 
                    target_col: str,
                    test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    # Data division
    divider = DataDivideStrategy()
    X_train, X_test, y_train, y_test = divider.handle_data(df, target_col, test_size)
    logging.info("Data split: train %d, test %d", len(X_train), len(X_test))
    
    return X_train, X_test, y_train, y_test

def encode_df(df_train: pd.DataFrame,
            df_test: Optional[pd.DataFrame] = None,  
            method: str = "onehot", 
            columns: List[str] = []) -> Union[pd.DataFrame, pd.Series]:
    encode_strategy = DataEncodeStrategy()
    
    return encode_strategy.handle_data(df_train, df_test, method, columns)

def normalize_df(df_train: pd.DataFrame,
                df_test: Optional[pd.DataFrame] = None, 
                method: str = "standard", 
                columns: Union[List[str], None] = None) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    normalize_strategy = DataNormalizeStrategy()
    
    return normalize_strategy.handle_data(df_train, df_test, method, columns)
    
def vectorize_text(df_train: pd.DataFrame,
                   df_test: Optional[pd.DataFrame] = None,
                   column: str = "",
                   max_features: int = 1000) -> Union[pd.DataFrame, Tuple[pd.DataFrame, pd.DataFrame]]:
    vectorize_strategy = TextVectorizeStrategy()
    df_train, df_test = vectorize_strategy.handle_data(df_train, df_test, column, max_features)
    logging.info("TF-IDF vectorization applied to column: %s", column)
    
    return df_train, df_test
