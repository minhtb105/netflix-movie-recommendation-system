from fastapi import APIRouter, HTTPException
from feast import FeatureStore
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
