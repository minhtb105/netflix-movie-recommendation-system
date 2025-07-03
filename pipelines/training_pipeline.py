from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
from steps.train_model import get_or_train
from src.model_dev import (
    PopularityBased, UserBasedCF, ItemBasedCF,
    PopularityPyFuncModel, UserCFPyfuncModel, ItemCFPyfuncModel,
    compute_user_item_matrix
)
from steps.fetch_features import (
    get_user_features_df,
    get_movie_features_df,
    get_rating_features_df,
)
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def save_user_item_matrix():
    df = get_rating_features_df()
    compute_user_item_matrix(df)

def top_n_rating_pipeline():
    df = get_rating_features_df()
    base_model = PopularityBased()
    base_model.train(df)
    model = PopularityPyFuncModel(model=base_model)
    get_or_train(model)

def user_based_cf_pipeline():
    base_model = UserBasedCF()
    base_model.train()
    model = UserCFPyfuncModel(model=base_model)
    get_or_train(model)

def item_based_cf_pipeline():
    base_model = ItemBasedCF()
    base_model.train()
    model = ItemCFPyfuncModel(model=base_model)
    get_or_train(model)
    