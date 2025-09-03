import pytest
import respx
from httpx import Response
from services.tmdb_service.api.tv_api import TVService

pytestmark = pytest.mark.asyncio

@respx.mock
async def test_fetch_tv_details():
    series_id = 999
    
    route = respx.get(
        f"https://api.themoviedb.org/3/tv/{series_id}").mock(
        return_value=Response(200, json={"id": series_id, "name": "TV Show"})
    )

    async with httpx.AsyncClient() as client:
        service = TVService(client=client)
        data = await service.fetch_tv_details(series_id)

    assert route.called
    assert data["id"] == series_id
    assert data["name"] == "TV Show"
