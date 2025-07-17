from src.base_client import TMDBBaseClient
from utils.downloader import async_batch_download_images
from typing import Any, Dict
from datetime import date, datetime


class MovieService(TMDBBaseClient):
    async def fetch_now_playing(self, language="en-US", page=1, region="VN"):
        # Get a list of movies that are currently in theatres.
        endpoint = "/movie/now_playing"
        params = {"language": language, "page": page, "region": region}
        
        return await self._get(endpoint, params)

    async def fetch_popular(self, language="en-US", page=1, region="VN"):
        # Get a list of movies ordered by popularity.
        endpoint = "/movie/popular"
        params = {"language": language, "page": page, "region": region}
        
        return await self._get(endpoint, params)

    async def fetch_top_rated(self, language="en-US", page=1, region="VN"):
        endpoint = "/movie/top_rated"
        params = {"language": language, "page": page, "region": region}
        
        return await self._get(endpoint, params)

    async def fetch_upcoming(self, language="en-US", page=1, region="VN"):
        endpoint = "/movie/upcoming"
        params = {"language": language, "page": page, "region": region}
        
        return await self._get(endpoint, params)

    async def fetch_movie_details(self, movie_id: int, language="en-US", include_image_language="en,null"):
        endpoint = f"/movie/{movie_id}"
        params = {
            "language": language,
            "append_to_response": "images,keywords,credits,providers",
            "include_image_language": include_image_language
        }
        
        return await self._get(endpoint, params)

    async def fetch_movie_reviews(self, movie_id: int, language="en-US", page: int = 1):
        endpoint = f"/movie/{movie_id}/reviews"
        params = {
            "language": language,
            "page": page
        }
        
        return await self._get(endpoint, params)

    async def fetch_recommendation_movies(self, movie_id: int, 
                                          language: str = "en-US", 
                                          page: int = 1):
        endpoint = f"/movie/{movie_id}/recommendations"
        params = {"language": language, "page": page}
        
        return await self._get(endpoint, params)

    async def fetch_similar_movies(self, movie_id: int, 
                                   language: str = "en-US", 
                                   page: int = 1):
        endpoint = f"/movie/{movie_id}/similar"
        params = {"language": language, "page": page}
        
        return await self._get(endpoint, params)

    async def fetch_changes(self, movie_id: int, 
                            end_date: date | datetime, 
                            start_date: date | datetime,
                            page: int = 1):
        endpoint = f"/movie/{movie_id}/changes"
        params = {"end_date": end_date, "page": page, "start_date": start_date}
        
        return await self._get(endpoint, params)
    
    async def fetch_trailers(self, movie_id: int, language: str = "en-US"):
        endpoint = f"/movie/{movie_id}/videos"
        params = {"language": language}
        
        return await self._get(endpoint, params)
           