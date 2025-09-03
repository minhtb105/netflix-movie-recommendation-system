import pytest
from httpx import HTTPStatusError
from services.tmdb_service.api.search_api import SearchService
from unittest.mock import AsyncMock

pytestmark = pytest.mark.asyncio

async def test_search_movie(monkeypatch):
    query = "Matrix"
    service = SearchService()

    monkeypatch.setattr(service, "_get", AsyncMock(return_value={
        "results": [{"id": 10, "title": "The Matrix"}]
    }))

    data = await service.search_movie(query=query)

    assert data["results"][0]["title"] == "The Matrix"

async def test_search_movie_404(monkeypatch):
    query = "Unknown Movie"
    service = SearchService()

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError(message="Not Found", request=None, response=None)

    monkeypatch.setattr(service, "_get", mock_get)

    with pytest.raises(HTTPStatusError):
        await service.search_movie(query=query)
