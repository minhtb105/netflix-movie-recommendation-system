import pandas as pd
from abc import ABC, abstractmethod
from typing import Union, List, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging


class DataStrategy(ABC):
    """
    Abstract class difining strategy for cleaning data
    """
    @abstractmethod
    def handle_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass


class DataPreprocessStrategy(DataStrategy):
    def handle_data(self, data: pd.DataFrame, datetime_cols: Optional[List[str]] = None) -> pd.DataFrame:
        try:
            # Drop duplicates or invalid data if any
            num_duplicates = data.duplicated().sum()
            na_pct = data.isna().mean()
            cols_to_drop = na_pct[na_pct > 0.8].index
            data = data.drop(columns=cols_to_drop)
                
            data.dropna(inplace=True, how='all')
            data.drop_duplicates(inplace=True)
            
            if datetime_cols is not None:
                for col in datetime_cols:
                    try:
                        data[col] = pd.to_datetime(data[col])
                    except Exception:
                        logging.error(f"Convert datetime error when in column {col}")
                    
            return data
        except Exception as e:
            logging.error(f"Error in preprocessing data: {e},")
            raise e
        
class DataDivideStrategy(DataStrategy):
    """
    Strategy for dividing data into train and test
    """ 
    def handle_data(self, data: pd.DataFrame, target_col: str, test_size: float = 0.2) -> Union[pd.DataFrame, pd.Series]:
        try:
            X = data.drop(target_col, axis=1)
            y = data[target_col]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
            
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error(f"Error in dividing data: {e}.")
            raise e
    
class DataEncodeStrategy(DataStrategy):
    """
    Strategy for encoding specific categorical features
    """
    def handle_data(self, df_train: pd.DataFrame,
                    df_test: Optional[pd.DataFrame] = None, 
                    method: str = "onehot", 
                    columns: List[str] = []) -> pd.DataFrame:
        if not columns:
            raise ValueError("You must specify at least one column to encode.")
        
        for col in columns:
            if col not in df_train.columns:
                raise ValueError(f"Column {col} not found in DataFrame.")
            
        if method == "label":
            for col in columns:
                le = LabelEncoder()
                df_train[col] = le.fit_transform(df_train[col].astype(str))
                if df_test is not None:
                    df_test[col] = le.transform(df_test[col].astype(str))
                
            return df_train, df_test
        elif method == "onehot":
            encoder = OneHotEncoder(
                handle_unknown='ignore',  
                sparse_output=False,          
            )

            df_train_cat = encoder.fit_transform(df_train[columns])
                
            new_cols = encoder.get_feature_names_out(columns)
            
            df_train_oh = pd.DataFrame(df_train_cat, columns=new_cols, 
                                       index=df_train.index)
            
            df_train = pd.concat([df_train.drop(columns, axis=1), df_train_oh], axis=1)
            
            if df_test is not None:
                df_test_cat = encoder.transform(df_test[columns])
                df_test_oh = pd.DataFrame(df_test_cat, 
                                          new_cols, 
                                          df_test.index)
                df_test = pd.concat([df_test.drop(columns, axis=1), df_test_oh], axis=1)
            
            return df_train, df_test
        else:
            raise ValueError("Unsupported encoding method. Use 'lable' or 'onehot'.")
    
class DataNormalizeStrategy(DataStrategy):
    def handle_data(self, df_train: pd.DataFrame,
                    df_test: Optional[pd.DataFrame] = None,
                    method: str = "standard", 
                    columns: Union[List[str], None] = None) -> pd.DataFrame:
        """
        :param method: 'standard' or 'minmax'
        :param columns: List of numeric column names to normalize. If None, auto-select numeric columns.
        """
        try:
            if columns is None:
                columns = df_train.select_dtypes(include=['number']).columns.tolist()
            
            if method == "standard":
                scaler = StandardScaler()
            elif method == "minmax":
                scaler = MinMaxScaler()
            else:
                    raise ValueError("Unsupported method. Choose 'standard' or 'minmax'.")

            df_train[columns] = scaler.fit_transform(df_train[columns])
            if df_test is not None:
                df_test[columns] = scaler.transform(df_test[columns])

            return df_train, df_test
        except Exception as e:
                logging.error(f"Error in normalizing data: {e}")
                raise e

class DataCleaning:
    def __init__(self, data: pd.DataFrame, strategy: DataStrategy):
        self.data = data
        self.strategy = strategy
        
    def handle_data(self) -> Union[pd.DataFrame, pd.Series]:
        try:
            return self.strategy.handle_data(self.data)
        except Exception as e:
            logging.error(f"Error while handling data: {e}.")
            raise e
         