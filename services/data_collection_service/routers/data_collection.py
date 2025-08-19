from fastapi import APIRouter, Query
import asyncio
from pathlib import Path
from pipelines import tmdb_metadata_pipelines as pipeline

router = APIRouter(prefix="/data-collection", tags=["Data Collection"])

@router.post("/collect-all")
async def collect_all_data(max_pages: int = Query(300, ge=1, le=1000)):
    """
    Collect metadata and images for both movies and TV shows from TMDB service.
    """
    movie_ids, tv_ids = await asyncio.gather(
        pipeline.fetch_movie_ids(max_pages=max_pages),
        pipeline.fetch_tv_ids(max_pages=max_pages)
    )

    movies_meta, tv_meta = await asyncio.gather(
        pipeline.fetch_movie_metadata(movie_ids, pipeline.RAW_DIR / "movies_metadata.json"),
        pipeline.fetch_tv_metadata(tv_ids, pipeline.RAW_DIR / "tv_metadata.json")
    )

    await asyncio.gather(
        pipeline.process_movie_images(movies_meta),
        pipeline.process_tv_images(tv_meta)
    )

    return {
        "movies_collected": len(movie_ids),
        "tv_collected": len(tv_ids),
        "movies_metadata_path": str(Path(pipeline.RAW_DIR) / "movies_metadata.json"),
        "tv_metadata_path": str(Path(pipeline.RAW_DIR) / "tv_metadata.json"),
    }


@router.post("/collect-movies")
async def collect_movies(max_pages: int = Query(300, ge=1, le=1000)):
    """
    Collect metadata and images only for movies.
    """
    movie_ids = await pipeline.fetch_movie_ids(max_pages=max_pages)
    movies_meta = await pipeline.fetch_movie_metadata(
        movie_ids, pipeline.RAW_DIR / "movies_metadata.json"
    )
    await pipeline.process_movie_images(movies_meta)

    return {
        "movies_collected": len(movie_ids),
        "movies_metadata_path": str(Path(pipeline.RAW_DIR) / "movies_metadata.json"),
    }


@router.post("/collect-tv")
async def collect_tv(max_pages: int = Query(300, ge=1, le=1000)):
    """
    Collect metadata and images only for TV shows.
    """
    tv_ids = await pipeline.fetch_tv_ids(max_pages=max_pages)
    tv_meta = await pipeline.fetch_tv_metadata(
        tv_ids, pipeline.RAW_DIR / "tv_metadata.json"
    )
    await pipeline.process_tv_images(tv_meta)

    return {
        "tv_collected": len(tv_ids),
        "tv_metadata_path": str(Path(pipeline.RAW_DIR) / "tv_metadata.json"),
    }
