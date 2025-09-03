import pytest
import respx
from httpx import Response
from services.tmdb_service.api.trending_api import TrendingService

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_fetch_trending_movies():
    route = respx.get(
        "https://api.themoviedb.org/3/trending/movie/day").mock(
        return_value=Response(200, json={"results": [{"id": 5, "title": "Trending Movie"}]})
    )

    async with httpx.AsyncClient() as client:
        service = TrendingService(client=client)
        data = await service.fetch_trending_movies()

    assert route.called
    assert data["results"][0]["title"] == "Trending Movie"
