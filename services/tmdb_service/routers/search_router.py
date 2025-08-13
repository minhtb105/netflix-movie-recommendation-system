from fastapi import APIRouter, Query
from .search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])
search_service = SearchService()

@router.get("/movie")
async def search_movie(
    query: str = Query(..., description="Search term for movies"),
    year: str = Query("2025"),
    language: str = Query("en-US"),
    page: int = Query(1, ge=1),
    region: str = Query("VN"),
    include_adult: bool = Query(False)
):
    return await search_service.search_movie(query, year, language, page, region, include_adult)

@router.get("/tv")
async def search_tv(
    query: str = Query(..., description="Search term for TV shows"),
    first_air_date_year: int = Query(2025),
    language: str = Query("en-US"),
    page: int = Query(1, ge=1),
    include_adult: bool = Query(False)
):
    return await search_service.search_tv(query, first_air_date_year, language, page, include_adult)

@router.get("/person")
async def search_person(
    query: str = Query(..., description="Search term for people"),
    language: str = Query("en-US"),
    page: int = Query(1, ge=1),
    include_adult: bool = Query(False)
):
    return await search_service.search_person(query, language, page, include_adult)

@router.get("/multi")
async def search_multi(
    query: str = Query(..., description="Search term for multiple categories"),
    language: str = Query("en-US"),
    page: int = Query(1, ge=1),
    include_adult: bool = Query(False)
):
    return await search_service.search_multi(query, language, page, include_adult)

@router.get("/find/{external_id}")
async def find_by_external_id(
    external_id: str,
    external_source: str = Query(..., description="External source type (e.g., imdb_id)")
):
    return await search_service.find_by_external_id(external_id, external_source)
