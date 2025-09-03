import pytest
import respx
from httpx import Response
from services.tmdb_service.api.search_api import SearchService

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_search_movie():
    query = "Matrix"
    service = SearchService()
    
    route = respx.get(
        "https://api.themoviedb.org/3/search/movie",
        client=service.client
    ).mock(
        return_value=Response(200, json={"results": [{"id": 10, "title": "The Matrix"}]})
    )

    data = await service.search_movie(query=query)

    assert route.called
    assert data["results"][0]["title"] == "The Matrix"
