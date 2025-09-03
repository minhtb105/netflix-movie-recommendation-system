import pytest
import respx
from httpx import Response
from services.collection_service import CollectionService

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_get_collection_details():
    collection_id = 321
    route = respx.get(f"https://api.themoviedb.org/3/collection/{collection_id}").mock(
        return_value=Response(200, json={"id": collection_id, "name": "Collection A"})
    )

    service = CollectionService()
    data = await service.get_collection_details(collection_id)

    assert route.called
    assert data["id"] == collection_id
    assert data["name"] == "Collection A"
