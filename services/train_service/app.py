from fastapi import FastAPI
from routers import train_router

app = FastAPI(title="Train Service")

app.include_router(train_router.router)
