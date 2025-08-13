from fastapi import APIRouter, Query
from services.movie_api import MovieService
from datetime import date

router = APIRouter()
service = MovieService()

@router.get("/movie/now_playing")
async def fetch_now_playing(
    language: str = Query("en-US"),
    page: int = Query(1),
    region: str = Query("VN")
):
    return await service.fetch_now_playing(language, page, region)

@router.get("/movie/popular")
async def fetch_popular(
    language: str = Query("en-US"),
    page: int = Query(1),
    region: str = Query("VN")
):
    return await service.fetch_popular(language, page, region)

@router.get("/movie/top_rated")
async def fetch_top_rated(
    language: str = Query("en-US"),
    page: int = Query(1),
    region: str = Query("VN")
):
    return await service.fetch_top_rated(language, page, region)

@router.get("/movie/upcoming")
async def fetch_upcoming(
    language: str = Query("en-US"),
    page: int = Query(1),
    region: str = Query("VN")
):
    return await service.fetch_upcoming(language, page, region)

@router.get("/movie/{movie_id}")
async def fetch_movie_details(
    movie_id: int,
    language: str = Query("en-US"),
    include_image_language: str = Query("en,null")
):
    return await service.fetch_movie_details(movie_id, language, include_image_language)

@router.get("/movie/{movie_id}/reviews")
async def fetch_movie_reviews(
    movie_id: int,
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await service.fetch_movie_reviews(movie_id, language, page)

@router.get("/movie/{movie_id}/recommendations")
async def fetch_recommendation_movies(
    movie_id: int,
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await service.fetch_recommendation_movies(movie_id, language, page)

@router.get("/movie/{movie_id}/similar")
async def fetch_similar_movies(
    movie_id: int,
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await service.fetch_similar_movies(movie_id, language, page)

@router.get("/movie/{movie_id}/changes")
async def fetch_changes(
    movie_id: int,
    end_date: date,
    start_date: date,
    page: int = Query(1)
):
    return await service.fetch_changes(movie_id, end_date, start_date, page)

@router.get("/movie/{movie_id}/videos")
async def fetch_trailers(
    movie_id: int,
    language: str = Query("en-US")
):
    return await service.fetch_trailers(movie_id, language)
