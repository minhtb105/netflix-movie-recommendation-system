import os
import logging
import asyncio
import httpx
import re
from typing import List


BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
TIME_OUT = int(os.getenv("TIME_OUT", 60))
MAX_CONCURRENT_DOWNLOADS = 2
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
common_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                  "Referer": "https://www.themoviedb.org/"}

async def download_image(
    client: httpx.AsyncClient,
    image_path: str,
    save_dir: str,
    movie_id: str = None,
    retries: int = 2
):
    if not image_path:
        logging.warning("Empty image path, skipping.")
        return

    url = f"{BASE_IMAGE_URL}{image_path}"
    file_name = f"{movie_id}.jpg"
    save_path = os.path.join(save_dir, file_name)

    for attempt in range(1, retries + 1):
        async with semaphore:
            logging.debug(f"[Attempt {attempt}] Downloading: {url}")
            response = await client.get(url, timeout=TIME_OUT)
            logging.debug(f"Status: {response.status_code}, headers: {response.headers}")

            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Downloaded image: {save_path}")
            else:
                logging.warning(f"[Attempt {attempt}] Failed to download {url}: {response.status_code}")
            return
        
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
            )
            for info in image_infos if info.get("image_path")
        ]
        await asyncio.gather(*tasks)
        
        
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
            id = cast.get("id")

            if not profile_path or not id:
                continue  

            task = download_image(
                client,
                image_path=profile_path,
                save_dir=save_dir,
                movie_id=id,
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
