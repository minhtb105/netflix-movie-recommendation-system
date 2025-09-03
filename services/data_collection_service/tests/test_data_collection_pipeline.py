from unittest.mock import AsyncMock
import pytest
from services.data_collection_service.pipelines import tmdb_metadata_pipelines as pipeline

@pytest.mark.asyncio
async def test_fetch_movie_ids_mock(monkeypatch):
    monkeypatch.setattr(pipeline.client, "_get", AsyncMock(return_value={"results": [{"id": 1}]}))
    ids = await pipeline.fetch_movie_ids(max_pages=1)
    assert ids == [1]
