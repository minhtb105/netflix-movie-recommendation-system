from fastapi import FastAPI
from routers import (
    features
)

app = FastAPI(title="Feature Retrieval Service")

app.include_router(features.router)
