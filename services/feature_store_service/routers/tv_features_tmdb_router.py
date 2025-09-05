from fastapi import APIRouter, HTTPException
from feast import FeatureStore
import pandas as pd
from schemas.tmdb_feature import TMDBFeatureRequest
from schemas.tmdb_feature import ReviewFeatureRequest
import os

router = APIRouter(prefix="/tv_features_tmdb", tags=["TV Features TMDB"])

store_path_2094 = os.path.join(os.path.dirname(__file__), "..", "store_2094")
store_path_384 = os.path.join(os.path.dirname(__file__), "..", "store_384")

fs_2094 = FeatureStore(repo_path=store_path_2094)
fs_384 = FeatureStore(repo_path=store_path_384)

@router.get("/features/{series_id}")
def get_tv_features(series_id: int):
    try:
        features = fs_2094.get_online_features(
            features=[
                "tv_features_tmdb:feature_vector",
                "tv_features_tmdb:vote_average",
                "tv_features_tmdb:vote_count",
                "tv_features_tmdb:video_key"
            ],
            entity_rows=[{"id": series_id}]
        ).to_dict()
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reviews/{series_id}")
def get_tv_reviews(series_id: int):
    try:
        reviews = fs_384.get_online_features(
            features=[
                "tv_reviews_tmdb:username",
                "tv_reviews_tmdb:content_vectorize",
                "tv_reviews_tmdb:rating"
            ],
            entity_rows=[{"id": series_id}]
        ).to_dict()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/features")
def add_tv_features(data: TMDBFeatureRequest):
    try:
        df = pd.DataFrame([data.dict()])
        fs_2094.write_to_online_store("tv_features_tmdb", df)
        return {"status": "success", "message": f"TV features for {data.id} stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reviews")
def add_tv_review(data: ReviewFeatureRequest):
    try:
        df = pd.DataFrame([data.dict()])
        fs_384.write_to_online_store("tv_reviews_tmdb", df)
        return {"status": "success", "message": f"Review for TV {data.id} stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    