from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
from steps.train_model import get_or_train
from src.model_dev import (
    PopularityBased, UserBasedCF, ItemBasedCF,
    PopularityPyFuncModel, UserCFPyfuncModel, ItemCFPyfuncModel
)
from steps.fetch_features import (
    get_user_features_df,
    get_movie_features_df,
    get_rating_features_df,
)

def top_n_rating_pipeline():
    df = get_rating_features_df()
    base_model = PopularityBased()
    model = PopularityPyFuncModel(model=base_model)
    get_or_train(model, df)

def user_based_cf_pipeline():
    df = get_rating_features_df()
    base_model = UserBasedCF()
    model = UserCFPyfuncModel(model=base_model)
    get_or_train(model, df)

def item_based_cf_pipeline():
    df = get_rating_features_df()
    base_model = ItemBasedCF()
    model = ItemCFPyfuncModel(model=base_model)
    get_or_train(model, df)

if __name__ == "__main__":
    top_n_rating_pipeline()
    user_based_cf_pipeline()
    item_based_cf_pipeline()
    