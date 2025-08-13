from fastapi import FastAPI
from routers import (
    collection_router,
    movie_router,
    search_router,
    trending_router,
    tv_router
)

app = FastAPI(title="TMDB Service")

app.include_router(collection_router.router)
app.include_router(movie_router.router)
app.include_router(search_router.router)
app.include_router(tv_router.router)
app.include_router(trending_router.router)
