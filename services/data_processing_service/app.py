from fastapi import FastAPI
from routers import (
    movielens_router,
    tmdb_router
)

app = FastAPI(title="TMDB Service")

app.include_router(movielens_router.router)
app.include_router(tmdb_router.router)
