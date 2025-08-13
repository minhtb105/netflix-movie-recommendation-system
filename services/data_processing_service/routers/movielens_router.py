from fastapi import APIRouter
from services.data_processing_service.pipelines.movies_pipeline_movielens import process_movies_pipeline
from services.data_processing_service.pipelines.ratings_pipeline_movielens import process_ratings_pipeline
from services.data_processing_service.pipelines.users_pipeline_movielens import process_users_pipeline
import traceback

router = APIRouter()

@router.post("/process-movies")
def process_movies():
    try:
        process_movies_pipeline()
        return {"status": "success", "message": "Movies processed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@router.post("/process_ratings")
def process_ratings():
    try:
        process_ratings_pipeline()
        return {"status": "success", "message": "Ratings processed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@router.post("/process_users")
def process_users():
    try:
        process_users_pipeline()
        return {"status": "success", "message": "Users processed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}
    