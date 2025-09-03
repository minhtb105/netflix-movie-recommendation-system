import pytest
from unittest.mock import AsyncMock
from httpx import HTTPStatusError
from services.tmdb_service.api.movie_api import MovieService

pytestmark = pytest.mark.asyncio

async def test_fetch_now_playing(monkeypatch):
    service = MovieService()

    monkeypatch.setattr(service, "_get", AsyncMock(return_value={
        "results": [{"id": 1, "title": "Movie A"}]
    }))

    data = await service.fetch_now_playing(page=2, region="US")

    assert data["results"][0]["title"] == "Movie A"
    assert "results" in data

async def test_fetch_movie_details(monkeypatch):
    movie_id = 123
    service = MovieService()

    monkeypatch.setattr(service, "_get", AsyncMock(return_value={
        "id": movie_id,
        "title": "Detail Movie"
    }))

    data = await service.fetch_movie_details(movie_id)

    assert data["id"] == movie_id
    assert data["title"] == "Detail Movie"

async def test_fetch_movie_details_404(monkeypatch):
    movie_id = 999

    service = MovieService()

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError(message="Not Found", request=None, response=None)

    monkeypatch.setattr(service, "_get", mock_get)

    with pytest.raises(HTTPStatusError):
        await service.fetch_movie_details(movie_id)
