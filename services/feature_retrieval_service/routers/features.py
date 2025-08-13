from fastapi import APIRouter, Query
from typing import List
from get_online_features import (
    get_user_features_online,
    get_movie_features_online,
    get_rating_features_online,
    get_movie_features_tmdb_online,
    get_movie_reviews_tmdb_online,
    get_tv_features_tmdb_online,
    get_tv_reviews_tmdb_online
)
from get_historical_features import (
    get_user_features_df,
    get_movie_features_df,
    get_rating_features_df,
    get_movie_features_tmdb_df,
    get_movie_reviews_tmdb_df,
    get_tv_features_tmdb_df,
    get_tv_reviews_tmdb_df
)

router = APIRouter(prefix="/features", tags=["Features"])

# ---------------- ONLINE FEATURES ----------------
@router.post("/online/users")
def online_user_features(user_ids: List[int] = Query(...)):
    df = get_user_features_online(user_ids)
    return df.to_dict(orient="records")

@router.post("/online/movies")
def online_movie_features(movie_ids: List[int] = Query(...)):
    df = get_movie_features_online(movie_ids)
    return df.to_dict(orient="records")

@router.post("/online/ratings")
def online_rating_features(user_ids: List[int] = Query(...), item_ids: List[int] = Query(...)):
    df = get_rating_features_online(user_ids, item_ids)
    return df.to_dict(orient="records")

@router.post("/online/movies_tmdb")
def online_movie_tmdb_features(movie_ids: List[int] = Query(...)):
    df = get_movie_features_tmdb_online(movie_ids)
    return df.to_dict(orient="records")

@router.post("/online/movie_reviews_tmdb")
def online_movie_tmdb_reviews(movie_ids: List[int] = Query(...)):
    df = get_movie_reviews_tmdb_online(movie_ids)
    return df.to_dict(orient="records")

@router.post("/online/tv_tmdb")
def online_tv_tmdb_features(tv_ids: List[int] = Query(...)):
    df = get_tv_features_tmdb_online(tv_ids)
    return df.to_dict(orient="records")

@router.post("/online/tv_reviews_tmdb")
def online_tv_tmdb_reviews(tv_ids: List[int] = Query(...)):
    df = get_tv_reviews_tmdb_online(tv_ids)
    return df.to_dict(orient="records")


# ---------------- HISTORICAL FEATURES ----------------
@router.get("/historical/users")
def historical_user_features():
    df = get_user_features_df()
    return df.to_dict(orient="records")

@router.get("/historical/movies")
def historical_movie_features():
    df = get_movie_features_df()
    return df.to_dict(orient="records")

@router.get("/historical/ratings")
def historical_rating_features():
    df = get_rating_features_df()
    return df.to_dict(orient="records")

@router.get("/historical/movies_tmdb")
def historical_movie_tmdb_features():
    df = get_movie_features_tmdb_df()
    return df.to_dict(orient="records")

@router.get("/historical/movie_reviews_tmdb")
def historical_movie_tmdb_reviews():
    df = get_movie_reviews_tmdb_df()
    return df.to_dict(orient="records")

@router.get("/historical/tv_tmdb")
def historical_tv_tmdb_features():
    df = get_tv_features_tmdb_df()
    return df.to_dict(orient="records")

@router.get("/historical/tv_reviews_tmdb")
def historical_tv_tmdb_reviews():
    df = get_tv_reviews_tmdb_df()
    return df.to_dict(orient="records")
