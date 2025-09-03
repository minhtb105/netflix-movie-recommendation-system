import os
import logging
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import httpx
import asyncio


class TMDBBaseClient:
    def __init__(self, max_concurrent_requests=5):
        self.token = os.getenv("TMDB_ACCESS_TOKEN")
        if not self.token:
            raise RuntimeError("TMDB_ACCESS_TOKEN is not set. Please set it in environment or .env")

        self.timeout = int(os.getenv("TIME_OUT", 10))
        self.base_api_url = "https://api.themoviedb.org/3"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        
        self.client = httpx.AsyncClient(timeout=self.timeout, headers=self.headers)
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(httpx.RequestError)
    )
    async def _get(self, endpoint: str, params: dict = None):
        url = f"{self.base_api_url}{endpoint}"
        async with self.semaphore:
            try:
                response = await self.client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP {e.response.status_code} for GET {url} - {e.response.text}")
                raise
            except httpx.RequestError as e:
                logging.error(f"RequestError for GET {url} - {e!r}")
                raise 

    async def close(self):
        await self.client.aclose()
