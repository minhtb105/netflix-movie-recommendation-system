from fastapi import FastAPI
from routers import recommend_router

app = FastAPI(title="Recommend Service")

app.include_router(recommend_router.router)
