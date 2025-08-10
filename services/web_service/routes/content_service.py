from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from utils.redis_helpers import get_item_from_redis
import redis


r = redis.Redis(host="localhost", port=6379, decode_responses=True)
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/movie/{movie_id}")
def movie_detail(movie_id: int, request: Request):
    movie = get_item_from_redis(r, "movie_id", movie_id)
    review = get_item_from_redis(r, "movie_review", movie_id)
    
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
    tv_df =  get_tv_features_tmdb_online([tv_id])
    review_df =  get_tv_reviews_tmdb_online([tv_id])

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