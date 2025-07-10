import os
import logging
import httpx
import asyncio
from typing import List


BASE_IMAGE_URL = "https://image.tmdb.org/t/p/original"
TIME_OUT = int(os.getenv("TIME_OUT", 10))
MAX_CONCURRENT_DOWNLOADS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

async def download_image(
    client: httpx.AsyncClient,
    image_path: str,
    save_dir: str,
    movie_id: str = None,
    img_type: str = None,
    retries: int = 3
):
    if not image_path:
        logging.warning("Empty image path, skipping.")
        return

    url = f"{BASE_IMAGE_URL}{image_path}"
    file_name = f"{movie_id}_{img_type}.jpg" if movie_id and img_type else os.path.basename(image_path)
    save_path = os.path.join(save_dir, file_name)

    for attempt in range(1, retries + 1):
        async with semaphore:
            try:
                logging.debug(f"[Attempt {attempt}] Downloading: {url}")
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()

                with open(save_path, 'wb') as f:
                    f.write(response.content)

                logging.info(f"Downloaded image: {save_path}")
                return
            except Exception as e:
                logging.warning(f"[{attempt}/{retries}] Failed to download {url}: {e}")
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
        