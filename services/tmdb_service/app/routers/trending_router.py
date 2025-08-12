from fastapi import APIRouter, Query
from .services.trending_service import TrendingService

router = APIRouter(prefix="/trending", tags=["Trending"])
service = TrendingService()

@router.get("/all/{time_window}")
async def get_trending_all(
    time_window: str,
    language: str = Query("en-US")
):
    """
    Get trending content (movies, TV, people) for a given time window ("day" or "week").
    """
    return await service.fetch_trending_all(time_window, language)

@router.get("/movies/{time_window}")
async def get_trending_movies(
    time_window: str,
    language: str = Query("en-US")
):
    """
    Get trending movies for a given time window ("day" or "week").
    """
    return await service.fetch_trending_movies(time_window, language)

@router.get("/tv/{time_window}")
async def get_trending_tv(
    time_window: str,
    language: str = Query("en-US")
):
    """
    Get trending TV shows for a given time window ("day" or "week").
    """
    return await service.fetch_trending_tv(time_window, language)

@router.get("/people/{time_window}")
async def get_trending_people(
    time_window: str,
    language: str = Query("en-US")
):
    """
    Get trending people for a given time window ("day" or "week").
    """
    return await service.fetch_trending_people(time_window, language)
