import pytest
import respx
from httpx import Response
import httpx
from services.tmdb_service.api.movie_api import MovieService

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_fetch_now_playing():
    # Mock endpoint
    route = respx.get("https://api.themoviedb.org/3/movie/now_playing").mock(
        return_value=Response(200, json={"results": [{"id": 1, "title": "Movie A"}]})
    )

    
    async with httpx.AsyncClient() as client:
        service = MovieService(client=client)
        data = await service.fetch_now_playing(page=2, region="US")

    assert route.called
    assert data["results"][0]["title"] == "Movie A"
    assert "results" in data


@respx.mock
async def test_fetch_movie_details():
    movie_id = 123
    
    route = respx.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}").mock(
        return_value=Response(200, json={"id": movie_id, "title": "Detail Movie"})
    )

    async with httpx.AsyncClient() as client:
        service = MovieService(client=client)
        data = await service.fetch_movie_details(movie_id)

    assert route.called
    assert data["id"] == movie_id
    assert data["title"] == "Detail Movie"
