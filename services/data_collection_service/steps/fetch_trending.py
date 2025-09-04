import asyncio
from services.trending_api import TrendingService

def fetch_trending_movie_ids():
    async def _run():
        service = TrendingService()
        data = await service.fetch_trending_movies()
        return [m['id'] for m in data['results']]
    
    return asyncio.run(_run())

def fetch_trending_tv_ids():
    async def _run():
        service = TrendingService()
        data = await service.fetch_trending_tv()
        
        return [tv['id'] for tv in data['results']]
    
    return asyncio.run(_run())
