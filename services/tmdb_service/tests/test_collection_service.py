import pytest
from unittest.mock import AsyncMock
from httpx import HTTPStatusError
from services.tmdb_service.api.collection_api import CollectionService

pytestmark = pytest.mark.asyncio

async def test_get_collection_details_success(monkeypatch):
    collection_id = 321
    service = CollectionService()

    monkeypatch.setattr(service, "_get", AsyncMock(return_value={
        "id": collection_id,
        "name": "Collection A"
    }))

    data = await service.get_collection_details(collection_id)

    assert data["id"] == collection_id
    assert data["name"] == "Collection A"

async def test_get_collection_details_404(monkeypatch):
    collection_id = 9999
    service = CollectionService()

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError(message="Not Found", request=None, response=None)

    monkeypatch.setattr(service, "_get", mock_get)

    with pytest.raises(HTTPStatusError):
        await service.get_collection_details(collection_id)

async def test_get_collection_details_500(monkeypatch):
    collection_id = 123
    service = CollectionService()

    async def mock_get(*args, **kwargs):
        raise HTTPStatusError(message="Internal server error", request=None, response=None)

    monkeypatch.setattr(service, "_get", mock_get)

    with pytest.raises(HTTPStatusError):
        await service.get_collection_details(collection_id)
