from clients.base_client import TMDBBaseClient
from datetime import date, datetime


class TVService(TMDBBaseClient):
    async def fetch_airing_today(self, language="en-US", page=1, timezone="Asia/Ho_Chi_Minh"):
        endpoint = "/tv/airing_today"
        params = {"language": language, "page": page, "timezone": timezone}
        
        return await self._get(endpoint, params)

    async def fetch_on_the_air(self, language="en-US", page=1, timezone="Asia/Ho_Chi_Minh"):
        endpoint = "/tv/on_the_air"
        params = {"language": language, "page": page, "timezone": timezone}
        
        return await self._get(endpoint, params)

    async def fetch_popular_tv(self, language="en-US", page=1):
        endpoint = "/tv/popular"
        params = {"language": language, "page": page}
        
        return await self._get(endpoint, params)

    async def fetch_top_rated_tv(self, language="en-US", page=1):
        endpoint = "/tv/top_rated"
        params = {"language": language, "page": page}
        
        return await self._get(endpoint, params)

    async def fetch_tv_details(self, series_id: int, language="en-US",
                        include_image_language="en,null"):
        endpoint = f"/tv/{series_id}"
        params = {
            "language": language,
            "append_to_response": "images,keywords,aggregate_credits,providers",
            "include_image_language": include_image_language
        }
        
        return await self._get(endpoint, params)

    async def fetch_tv_reviews(self,series_id: int, language="en-US", page: int = 1):
        endpoint = f"/tv/{series_id}/reviews"
        params = {
            "language": language,
            "page": page
        }
        
        return await self._get(endpoint, params)

    async def fetch_tv_recommendations(self, series_id: int, language="en-US", page=1):
        endpoint = f"/tv/{series_id}/recommendations"
        params = {"language": language, "page": page}
        
        return await self._get(endpoint, params)

    async def fetch_similar_tv(self, series_id: int, language="en-US", page=1):
        endpoint = f"/tv/{series_id}/similar"
        params = {"language": language, "page": page}
        
        return await self._get(endpoint, params)

    async def fetch_watch_providers(self, series_id: int):
        endpoint = f"/tv/{series_id}/watch/providers"
        
        return await self._get(endpoint)

    async def fetch_changes(self, series_id: int,
                            end_date: date | datetime,
                            start_date: date | datetime,
                            page: int = 1):
        endpoint = f"/tv/{series_id}/changes"
        params = {"end_date": end_date, "page": page, "start_date": start_date}
        
        return await self._get(endpoint, params)
        
    async def fetch_tv_trailers(self, series_id: int, 
                               include_video_language: str = "en-US"):
        endpoint = f"/tv/{series_id}/videos"
        params = {"include_video_language": include_video_language}
        
        return await self._get(endpoint, params)
    