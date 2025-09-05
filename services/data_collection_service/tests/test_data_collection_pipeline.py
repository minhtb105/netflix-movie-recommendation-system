from unittest.mock import AsyncMock
import pytest
from pipelines import tmdb_metadata_pipelines as pipeline
import os, sys


_service_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _service_root not in sys.path:
    sys.path.insert(0, _service_root)
        
@pytest.mark.asyncio
async def test_fetch_movie_ids_mock(monkeypatch):
    monkeypatch.setattr(pipeline.client, "_get", AsyncMock(return_value={"results": [{"id": 1}]}))
    ids = await pipeline.fetch_movie_ids(max_pages=1)
    assert ids == [1]
