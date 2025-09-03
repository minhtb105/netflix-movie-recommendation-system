from clients.base_client import TMDBBaseClient


class TrendingService(TMDBBaseClient):
    async def fetch_trending_all(self, time_window="day", language="en-US"):
        endpoint = f"/trending/all/{time_window}"
        params = {"language": language}
        
        return await self._get(endpoint, params)

    async def fetch_trending_movies(self, time_window="day", language="en-US"):
        endpoint = f"/trending/movie/{time_window}"
        params = {"language": language}
        
        return await self._get(endpoint, params)

    async def fetch_trending_tv(self, time_window="day", language="en-US"):
        endpoint = f"/trending/tv/{time_window}"
        params = {"language": language}
        
        return await self._get(endpoint, params)

    async def fetch_trending_people(self, time_window="day", language="en-US"):
        endpoint = f"/trending/person/{time_window}"
        params = {"language": language}
        
        return await self._get(endpoint, params)
