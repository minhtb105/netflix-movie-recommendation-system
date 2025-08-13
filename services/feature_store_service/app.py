from fastapi import FastAPI
from routers import (
    movie_features_tmdb_router,
    movie_features_router,
    rating_features_router,
    tv_features_tmdb_router,
    user_features_router
)

app = FastAPI(title="Feature Store Service")

# Include routers
app.include_router(movie_features_tmdb_router.router)
app.include_router(movie_features_router.router)
app.include_router(rating_features_router.router)
app.include_router(tv_features_tmdb_router.router)
app.include_router(user_features_router.router)
