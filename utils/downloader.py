import os
import logging
import asyncio
import httpx
import re
import backoff
from typing import List
from httpx import RequestError, HTTPStatusError


BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w300"
TIME_OUT = int(os.getenv("TIME_OUT", 20))
MAX_CONCURRENT_DOWNLOADS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
_not_found_cache = set()
common_headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.themoviedb.org/",
}

async def _url_exists(client: httpx.AsyncClient, url: str) -> bool:
    try: 
        resp = client.head(url, timeout=TIME_OUT)
        
        return resp.status_code == 200
    except Exception:
        return False
    
    
@backoff.on_exception(
    backoff.expo,
    (RequestError, HTTPStatusError),
    max_tries=5,
    jitter=backoff.full_jitter
)
async def download_image(
    client: httpx.AsyncClient,
    image_path: str,
    save_dir: str,
    movie_id: str = None,
    img_type: str = None,
):
    if not image_path:
        logging.warning("Empty image path, skipping.")
        return

    url = f"{BASE_IMAGE_URL}{image_path}"
    if url in _not_found_cache:
        logging.debug(f"Skipping cached-404 URL: {url}")
        return

    # 1) HEAD check
    if not await _url_exists(client, url):
        logging.warning(f"Image not found (404): {url}")
        _not_found_cache.add(url)
        return

    # 2) Download with retries via backoff
    async with semaphore:
        response = await client.get(url, timeout=TIME_OUT)
        response.raise_for_status()

        file_name = f"{movie_id}_{img_type}.jpg" if movie_id and img_type else os.path.basename(image_path)
        save_path = os.path.join(save_dir, file_name)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Downloaded image: {save_path}")


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

    async with httpx.AsyncClient(
        headers=common_headers,
        timeout=httpx.Timeout(TIME_OUT),
        limits=httpx.Limits(max_connections=MAX_CONCURRENT_DOWNLOADS)
    ) as client:
        tasks = [
            download_image(
                client,
                info.get("image_path"),
                save_dir,
                movie_id=info.get("movie_id"),
                img_type=info.get("img_type")
            )
            for info in image_infos if info.get("image_path")
        ]
        await asyncio.gather(*tasks)

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    
    return re.sub(r'[\s_-]+', '_', name)

async def download_cast_images(cast_list: List[dict], save_dir: str = "app/static/images/cast"):
    """
    Download profile images of cast members.
    
    Args:
        cast_list (List[dict]): Each dict must include:
            - name (str): Actor's name (used for filename)
            - profile_path (str): Image path from TMDB
        save_dir (str): Directory to save images.
    """
    os.makedirs(save_dir, exist_ok=True)

    async with httpx.AsyncClient(
        headers=common_headers,
        timeout=httpx.Timeout(TIME_OUT),
        limits=httpx.Limits(max_connections=MAX_CONCURRENT_DOWNLOADS)
    ) as client:
        tasks = []

        for cast in cast_list:
            profile_path = cast.get("profile_path")
            name = cast.get("name")

            if not profile_path or not name:
                continue  

            sanitized_name = sanitize_filename(name)
            save_path = os.path.join(save_dir, f"{sanitized_name}.jpg")

            task = download_image(
                client,
                image_path=profile_path,
                save_dir=save_dir,
                movie_id=sanitized_name, 
                img_type=None  
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

