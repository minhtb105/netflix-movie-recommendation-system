from fastapi import FastAPI
from routers import (
    data_collection,
    health,
)

app = FastAPI(title="Data Collection Service")

app.include_router(data_collection.router)
app.include_router(health.router)
