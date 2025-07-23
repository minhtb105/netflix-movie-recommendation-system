from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from steps.fetch_features import (
    get_movie_features_tmdb_df,
    get_movie_reviews_tmdb_df,
    get_tv_features_tmdb_df,
    get_tv_reviews_tmdb_df
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/movie/{movie_id}")
def movie_detail(movie_id: int, request: Request):
    movie_df = get_movie_features_tmdb_df()
    review_df = get_movie_reviews_tmdb_df()

    movie = movie_df[movie_df["id"] == movie_id].to_dict(orient="records")
    review = review_df[review_df["id"] == movie_id].to_dict(orient="records")
    
    if not movie:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    return templates.TemplateResponse(
        "movie_detail.html",
        {
            "request": request,
            "movie": movie[0],          
            "review": review[0] if review else None
        }
    )

@router.get("/tv/{tv_id}")
def tv_detail(tv_id: int, request: Request):
    tv_df = get_tv_features_tmdb_df()
    review_df = get_tv_reviews_tmdb_df()

    tv = tv_df[tv_df["id"] == tv_id].to_dict(orient="records")
    review = review_df[review_df["id"] == tv_id].to_dict(orient="records")

    if not tv:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    return templates.TemplateResponse(
        "tv_detail.html",
        {
            "request": request,
            "tv": tv[0],                 
            "review": review[0] if review else None
        }
    )