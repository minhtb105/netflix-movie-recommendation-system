from fastapi import APIRouter, Query
from services.tv_api import TVService
from datetime import date

router = APIRouter(prefix="/tv", tags=["TV"])

tv_service = TVService()

@router.get("/airing_today")
async def get_airing_today(
    language: str = Query("en-US"),
    page: int = Query(1),
    timezone: str = Query("Asia/Ho_Chi_Minh")
):
    return await tv_service.fetch_airing_today(language, page, timezone)


@router.get("/on_the_air")
async def get_on_the_air(
    language: str = Query("en-US"),
    page: int = Query(1),
    timezone: str = Query("Asia/Ho_Chi_Minh")
):
    return await tv_service.fetch_on_the_air(language, page, timezone)


@router.get("/popular")
async def get_popular_tv(
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await tv_service.fetch_popular_tv(language, page)


@router.get("/top_rated")
async def get_top_rated_tv(
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await tv_service.fetch_top_rated_tv(language, page)


@router.get("/{series_id}")
async def get_tv_details(
    series_id: int,
    language: str = Query("en-US"),
    include_image_language: str = Query("en,null")
):
    return await tv_service.fetch_tv_details(series_id, language, include_image_language)


@router.get("/{series_id}/reviews")
async def get_tv_reviews(
    series_id: int,
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await tv_service.fetch_tv_reviews(series_id, language, page)


@router.get("/{series_id}/recommendations")
async def get_tv_recommendations(
    series_id: int,
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await tv_service.fetch_tv_recommendations(series_id, language, page)


@router.get("/{series_id}/similar")
async def get_similar_tv(
    series_id: int,
    language: str = Query("en-US"),
    page: int = Query(1)
):
    return await tv_service.fetch_similar_tv(series_id, language, page)


@router.get("/{series_id}/watch/providers")
async def get_watch_providers(series_id: int):
    return await tv_service.fetch_watch_providers(series_id)


@router.get("/{series_id}/changes")
async def get_changes(
    series_id: int,
    end_date: date,
    start_date: date,
    page: int = Query(1)
):
    return await tv_service.fetch_changes(series_id, end_date, start_date, page)


@router.get("/{series_id}/trailers")
async def get_tv_trailers(
    series_id: int,
    include_video_language: str = Query("en-US")
):
    return await tv_service.fetch_tv_trailers(series_id, include_video_language)
