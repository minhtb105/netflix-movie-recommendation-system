import os
import logging
import asyncio
import httpx
import aiofiles
from typing import List


BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w300"
TIME_OUT = int(os.getenv("TIME_OUT", 30))
MAX_CONCURRENT_DOWNLOADS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
common_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                  "Referer": "https://www.themoviedb.org/"}
downloaded_images_cache = set()

async def download_image(
    client: httpx.AsyncClient,
    image_path: str,
    save_dir: str,
    id: int,
    retries: int = 2
):
    if not image_path:
        logging.warning("Empty image path, skipping.")
        return

    if not id:
        logging.warning("No id provided, skipping.")
        return

    url = f"{BASE_IMAGE_URL}{image_path}"
    file_name = f"{id}.jpg"
    save_path = os.path.join(save_dir, file_name)

    cache_key = os.path.abspath(save_path)
    if cache_key in downloaded_images_cache:
        logging.debug(f"Image in cache, skipping: {save_path}")
        return

    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        logging.debug(f"Image exists, skipping: {save_path}")
        downloaded_images_cache.add(cache_key) 
        return

    for attempt in range(1, retries + 1):
        async with semaphore:
            try:
                async with client.stream("GET", url, timeout=TIME_OUT) as response:
                    if response.status_code == 200:
                        async with aiofiles.open(save_path, 'wb') as f:
                            async for chunk in response.aiter_bytes():
                                await f.write(chunk)
                        logging.debug(f"Saving image as {save_path} (from {image_path}, id={id})")
                        downloaded_images_cache.add(cache_key)
                        return 
                    else:
                        logging.warning(f"[Attempt {attempt}] Failed to download {url}: {response.status_code}")
            except Exception as e:
                logging.error(f"[Attempt {attempt}] Exception while downloading {url}: {e}")
        
        await asyncio.sleep(2 ** attempt)  # exponential backoff

    logging.error(f"Failed after {retries} attempts: {url}")


async def async_batch_download_images(image_infos: List[dict], save_dir: str):
    """
    Download multiple images asynchronously.

    Args:
        image_infos (List[dict]): Each dict must include:
            - image_path (str)
            - movie_id (str or int), optional
            - img_type (str), optional ("poster", "backdrop", etc.)
        save_dir (str): Local directory to save images.
    """
    os.makedirs(save_dir, exist_ok=True)
    transport = httpx.AsyncHTTPTransport(retries=2)
    
    async with httpx.AsyncClient(
        headers=common_headers,
        timeout=httpx.Timeout(TIME_OUT),
        limits=httpx.Limits(max_connections=MAX_CONCURRENT_DOWNLOADS),
        transport=transport
    ) as client:
        tasks = [
            download_image(
                client,
                info.get("image_path"),
                save_dir,
                id=info.get("movie_id"),
            )
            for info in image_infos if info.get("image_path")
        ]
        await asyncio.gather(*tasks)
        
      
async def download_cast_image(client: httpx.AsyncClient, cast: dict, save_dir: str = "app/static/images/cast"):
    os.makedirs(save_dir, exist_ok=True)
    profile_path = cast.get("profile_path")
    id = cast.get("id")

    if not profile_path or not id:
        return

    await download_image(
        client=client,
        image_path=profile_path,
        save_dir=save_dir,
        id=str(id),
    )
        
async def download_cast_images_batch(cast_lists: List[dict], save_dir: str = "app/static/images/cast"):
    os.makedirs(save_dir, exist_ok=True)
    transport = httpx.AsyncHTTPTransport(retries=2)
    
    async with httpx.AsyncClient(
        http2=True,
        headers=common_headers,
        timeout=httpx.Timeout(TIME_OUT),
        limits=httpx.Limits(max_connections=MAX_CONCURRENT_DOWNLOADS),
        transport=transport
    ) as client:

        tasks = []
        for cast in cast_lists:
            tasks.append(download_cast_image(client, cast, save_dir))

        await asyncio.gather(*tasks)
        
