import pytest
from httpx import HTTPStatusError
from services.tmdb_service.api.trending_api import TrendingService
from unittest.mock import AsyncMock

pytestmark = pytest.mark.asyncio

async def test_fetch_trending_movies(monkeypatch):
    service = TrendingService()

    monkeypatch.setattr(service, "_get", AsyncMock(return_value={
        "results": [{"id": 5, "title": "Trending Movie"}]
    }))

    data = await service.fetch_trending_movies()

    assert data["results"][0]["title"] == "Trending Movie"

async def test_fetch_trending_movies_404(monkeypatch):
    service = TrendingService()

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError(message="Not Found", request=None, response=None)

    monkeypatch.setattr(service, "_get", mock_get)

    with pytest.raises(HTTPStatusError):
        await service.fetch_trending_movies()

