from fastapi import APIRouter, BackgroundTasks, Query
from pipelines.training_pipeline import (
    save_user_item_matrix,
    user_based_cf_pipeline,
    item_based_cf_pipeline,
    content_based_filtering_pipeline
)
from pipelines.evaluation_pipeline import evaluation_pipeline
import mlflow
import pandas as pd

router = APIRouter(prefix="/train", tags=["Training & Evaluation"])


@router.post("/save-user-item-matrix")
async def save_matrix(background_tasks: BackgroundTasks):
    """
    Create and save the user-item matrix for collaborative filtering.
    Runs in background.
    """
    background_tasks.add_task(save_user_item_matrix)
    return {"message": "User-Item matrix creation started."}


@router.post("/user-based-cf")
async def train_user_cf(background_tasks: BackgroundTasks):
    """
    Train User-Based Collaborative Filtering model.
    """
    background_tasks.add_task(user_based_cf_pipeline)
    return {"message": "User-Based CF training started."}


@router.post("/item-based-cf")
async def train_item_cf(background_tasks: BackgroundTasks):
    """
    Train Item-Based Collaborative Filtering model.
    """
    background_tasks.add_task(item_based_cf_pipeline)
    return {"message": "Item-Based CF training started."}


@router.post("/content-based-filtering")
async def train_content_based(background_tasks: BackgroundTasks):
    """
    Train Content-Based Filtering model.
    """
    background_tasks.add_task(content_based_filtering_pipeline)
    return {"message": "Content-Based Filtering training started."}


@router.post("/evaluate")
async def evaluate_model(
    model_name: str = Query(..., description="Name of the model to evaluate"),
    k: int = Query(10, description="Top-K for evaluation metrics")
):
    """
    Run evaluation for a given trained model.
    """
    model = mlflow.pyfunc.load_model(model_name)
    X_test = pd.read_parquet("data/X_test.parquet")
    y_test = pd.read_parquet("data/y_test.parquet")

    evaluation_pipeline(model, X_test, y_test, k=k)
    return {"message": f"Evaluation completed for model {model_name}."}
