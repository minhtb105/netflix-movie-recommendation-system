from fastapi import APIRouter, BackgroundTasks
from pipelines.movies_pipeline_tmdb import process_movies_pipeline
from pipelines.tv_pipeline_tmdb import process_tv_pipeline
import traceback

router = APIRouter(prefix="/tmdb", tags=["TMDB Data Processing"])

@router.post("/process-movies")
def process_tmdb_movies(background_tasks: BackgroundTasks):
    """
    Trigger processing for TMDB movie metadata and reviews.
    Runs in background to avoid blocking API response.
    """
    background_tasks.add_task(process_movies_pipeline)
    
    return {"status": "started", "message": "Movie processing started in background"}

@router.post("/process-tv")
def process_tmdb_tv(background_tasks: BackgroundTasks):
    """
    Trigger processing for TMDB TV metadata and reviews.
    Runs in background to avoid blocking API response.
    """
    background_tasks.add_task(process_tv_pipeline)
    
    return {"status": "started", "message": "TV processing started in background"}

@router.post("/process-all")
def process_tmdb_all(background_tasks: BackgroundTasks):
    """
    Trigger processing for both TMDB movies and TV in parallel.
    """
    background_tasks.add_task(process_movies_pipeline)
    background_tasks.add_task(process_tv_pipeline)
    
    return {"status": "started", "message": "Movies and TV processing started in background"}
