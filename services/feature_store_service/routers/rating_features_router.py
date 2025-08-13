from fastapi import APIRouter, HTTPException
from feast import FeatureStore
import os

router = APIRouter(prefix="/rating_features", tags=["Rating Features"])

store_path = os.path.dirname(__file__)
fs = FeatureStore(repo_path=store_path)

@router.get("/train")
def get_train_rating(user_id: int, item_id: int):
    try:
        features = fs.get_online_features(
            features=["X_train_rating:" + f for f in [
                "timestamp_year", "timestamp_month", "timestamp_day",
                "timestamp_hour", "timestamp_dayofweek", "timestamp_is_weekend",
                "time_since_last", "rating"
            ]],
            entity_rows=[{"user_id": user_id, "item_id": item_id}]
        ).to_dict()
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
def get_test_rating(user_id: int, item_id: int):
    try:
        features = fs.get_online_features(
            features=["X_test_rating:" + f for f in [
                "timestamp_year", "timestamp_month", "timestamp_day",
                "timestamp_hour", "timestamp_dayofweek", "timestamp_is_weekend",
                "time_since_last", "rating"
            ]],
            entity_rows=[{"user_id": user_id, "item_id": item_id}]
        ).to_dict()
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
