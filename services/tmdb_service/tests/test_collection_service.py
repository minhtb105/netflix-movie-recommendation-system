import pytest
import respx
from httpx import Response
import httpx
from services.tmdb_service.api.collection_service import CollectionService

pytestmark = pytest.mark.asyncio
service = CollectionService()

@respx.mock
async def test_get_collection_details():
    collection_id = 321
    route = respx.get(f"https://api.themoviedb.org/3/collection/{collection_id}").mock(
        return_value=Response(200, json={"id": collection_id, "name": "Collection A"})
    )

    data = await service.get_collection_details(collection_id)

    assert route.called
    assert data["id"] == collection_id
    assert data["name"] == "Collection A"

@pytest.mark.asyncio
async def test_get_collection_details_404():
    collection_id = 9999
    route = respx.get(f"https://api.themoviedb.org/3/collection/{collection_id}").mock(
        return_value=Response(404, json={"status_message": "Not Found"})
    )

   
    with pytest.raises(httpx.HTTPStatusError):
        await service.get_collection_details(collection_id)

    assert route.called
    await service.close()

@pytest.mark.asyncio
async def test_get_collection_details_500():
    collection_id = 123
    route = respx.get(f"https://api.themoviedb.org/3/collection/{collection_id}").mock(
        return_value=Response(500, json={"status_message": "Internal server error"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        await service.get_collection_details(collection_id)

    assert route.called
    await service.close()
