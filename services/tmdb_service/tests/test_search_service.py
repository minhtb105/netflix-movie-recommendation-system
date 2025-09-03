import pytest
import respx
from httpx import Response
from services.search_service import SearchService

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_search_movie():
    query = "Matrix"
    route = respx.get("https://api.themoviedb.org/3/search/movie").mock(
        return_value=Response(200, json={"results": [{"id": 10, "title": "The Matrix"}]})
    )

    service = SearchService()
    data = await service.search_movie(query=query)

    assert route.called
    assert data["results"][0]["title"] == "The Matrix"
