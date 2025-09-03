import pytest
from httpx import HTTPStatusError
from services.tmdb_service.api.tv_api import TVService
from unittest.mock import AsyncMock

pytestmark = pytest.mark.asyncio

async def test_fetch_tv_details(monkeypatch):
    series_id = 999
    service = TVService()

    monkeypatch.setattr(service, "_get", AsyncMock(return_value={
        "id": series_id,
        "name": "TV Show"
    }))

    data = await service.fetch_tv_details(series_id)

    assert data["id"] == series_id
    assert data["name"] == "TV Show"


async def test_fetch_tv_details_404(monkeypatch):
    series_id = 9999
    service = TVService()

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError(message="Not Found", request=None, response=None)

    monkeypatch.setattr(service, "_get", mock_get)

    with pytest.raises(HTTPStatusError):
        await service.fetch_tv_details(series_id)
