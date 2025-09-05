from fastapi import APIRouter, HTTPException
from feast import FeatureStore
from schemas.tmdb_feature import TMDBFeatureRequest
from schemas.tmdb_feature import ReviewFeatureRequest
import os


router = APIRouter(prefix="/movie_features_tmdb", tags=["Movie Features TMDB"])

# Load FeatureStore from repo path
store_path_2901 = os.path.join(os.path.dirname(__file__).parent[1], "/store_2901")
store_path_384 = os.path.join(os.path.dirname(__file__).parent[1], "/store_384")

fs_2901 = FeatureStore(repo_path=store_path_2901)
fs_384 = FeatureStore(repo_path=store_path_384)

@router.get("/features/{movie_id}")
def get_movie_features(movie_id: int):
    try:
        features = fs_2901.get_online_features(
            features=[
                "movie_features_tmdb:feature_vector",
                "movie_features_tmdb:vote_average",
                "movie_features_tmdb:vote_count",
                "movie_features_tmdb:video_key"
            ],
            entity_rows=[{"id": movie_id}]
        ).to_dict()
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reviews/{movie_id}")
def get_movie_reviews(movie_id: int):
    try:
        reviews = fs_384.get_online_features(
            features=[
                "movie_reviews_tmdb:username",
                "movie_reviews_tmdb:content_vectorize",
                "movie_reviews_tmdb:rating"
            ],
            entity_rows=[{"id": movie_id}]
        ).to_dict()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/features/movie")
def add_movie_feature(data: MovieFeatureRequest):
    try:
        df = pd.DataFrame([{
            "id": data.id,
            "feature_vector": data.feature_vector,
            "vote_average": data.vote_average,
            "vote_count": data.vote_count,
            "video_key": data.video_key,
            "event_timestamp": data.event_timestamp
        }])

        fs_2901.write_to_online_store("movie_features_tmdb", df)

        return {"status": "success", "message": f"Movie {data.id} feature stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/features/review")
def add_movie_reeview(data: ReviewFeatureRequest):
    try:
        df = pd.DataFrame([{
            "id": data.id,
            "username": data.username,
            "content_vectorize": data.content_vectorize,
            "rating": data.rating,
            "event_timestamp": data.event_timestamp
        }])

        fs_384.write_to_online_store("movie_reviews_tmdb", df)

        return {"status": "success", "message": f"Movie {data.id} review stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))