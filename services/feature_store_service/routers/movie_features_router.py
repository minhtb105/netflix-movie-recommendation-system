from fastapi import APIRouter, HTTPException
from feast import FeatureStore
import os

router = APIRouter(prefix="/movie_features_movielens", tags=["Movie Features Movielens"])

store_path_1000 = os.path.join(os.path.dirname(__file__), "..", "store_1000")
fs_1000 = FeatureStore(repo_path=store_path_1000)

@router.get("/{movie_id}")
def get_movie_features_movielens(movie_id: int):
    try:
        features = fs_1000.get_online_features(
            features=["movie_features_movielens:" + f for f in [
                "unknown", "Action", "Adventure", "Animation", "Childrens",
                "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                "Film_Noir", "Horror", "Musical", "Mystery", "Romance",
                "Sci_Fi", "Thriller", "War", "Western",
                "release_date_year", "release_date_month", "release_date_day",
                "release_date_hour", "release_date_dayofweek", "release_date_is_weekend",
                "title_tfidf"
            ]],
            entity_rows=[{"movie_id": movie_id}]
        ).to_dict()
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
