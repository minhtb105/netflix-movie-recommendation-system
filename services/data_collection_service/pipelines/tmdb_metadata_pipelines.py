import os
import asyncio
import json
import httpx
from pathlib import Path
from pybloom_live import BloomFilter
from services.data_collection_service.clients.tmdb_service_client import (
    TMDBServiceClient
)
from services.data_collection_service.utils.downloader import (
    download_single_image,
    download_single_cast_image,
)


client = TMDBServiceClient()

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

MOVIE_OUT = DATA_DIR / "movies.ndjson"
TV_OUT = DATA_DIR / "tv.ndjson"

NUM_WORKERS = 5
NUM_IMAGE_WORKERS = 3
QUEUE_MAXSIZE = 100
RATE_LIMIT_DELAY = 0.25
RETRY = 3
TIME_OUT = int(os.getenv("TIME_OUT", 30))

BASE_STATIC_DIR = Path(
    os.getenv(
        "STATIC_IMAGE_DIR",
        Path(__file__).resolve().parents[2] / "web_service" / "static" / "images"
    )
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.themoviedb.org/"
}


# =========================
# Producer
# =========================
async def produce_ids(queue: asyncio.Queue, endpoints, key="id", max_pages=1000):
    bloom = BloomFilter(capacity=100_000, error_rate=0.01)
    
    for endpoint in endpoints:
        for page in range(1, max_pages + 1):
            first_page = await client._get(endpoint, params={"page": page})

            if not first_page or "results" not in first_page:
                continue
            
            total_pages = min(first_page.get("total_pages", 1), max_pages)
            
            # handle page 1
            for item in first_page["results"]:
                _id = item["id"]
                    
                # deduplicate id
                if _id in bloom:
                    continue
                    
                bloom.add(_id)
                await queue.put(_id)

            for page in range(2, total_pages + 1):
                data = await client._get(endpoint, params={"page": page})

                if data and "results" in data:
                    for item in data["results"]:
                        _id = item[key]
                        if _id not in bloom:
                            bloom.add(_id)
                            await queue.put(_id)

                await asyncio.sleep(RATE_LIMIT_DELAY)

    # stop signal
    for _ in range(NUM_WORKERS):
        await queue.put(None)


# =========================
# Retry
# =========================
async def fetch_with_retry(url):
    for attempt in range(RETRY):
        try:
            res = await client._get(url)
            if res:
                return res
        except Exception:
            pass

        await asyncio.sleep(0.5 * (attempt + 1))

    return None


# =========================
# Extract image info
# =========================
def extract_images(entity, meta):
    images = []
    casts = []

    if not meta or not meta.get("details"):
        return images, casts

    details = meta["details"]

    # poster
    if details.get("poster_path"):
        images.append({
            "type": entity,
            "path": details["poster_path"],
            "id": meta["id"]
        })

    # cast
    credit_key = "credits" if entity == "movie" else "aggregate_credits"
    casts_info = details.get(credit_key, {}).get("cast", [])

    filtered = [
        {
            "id": c.get("id"),
            "profile_path": c.get("profile_path"),
            "popularity": c.get("popularity", 0),
        }
        for c in casts_info
        if c.get("profile_path")
        and "uncredited" not in (c.get("character") or "").lower()
        and "voice" not in (c.get("character") or "").lower()
    ]

    top_casts = sorted(filtered, key=lambda x: x["popularity"], reverse=True)[:3]
    casts.extend(top_casts)

    return images, casts


# =========================
# Worker (generic)
# =========================
async def worker(entity, id_queue, write_queue, image_queue):
    while True:
        item_id = await id_queue.get()

        if item_id is None:
            await write_queue.put(None)
            break

        details, videos, reviews = await asyncio.gather(
            fetch_with_retry(f"{entity}/{item_id}"),
            fetch_with_retry(f"{entity}/{item_id}/videos"),
            fetch_with_retry(f"{entity}/{item_id}/reviews"),
        )

        meta = {
            "id": item_id,
            "details": details,
            "videos": videos,
            "reviews": reviews,
        }
        
        id_queue.task_done()

        # write metadata
        await write_queue.put(meta)

        # extract images
        images, casts = extract_images(entity, meta)

        # poster images
        for img in images:
            await image_queue.put(("poster", img))

        # cast images
        for c in casts:
            await image_queue.put(("cast", c))

        await asyncio.sleep(RATE_LIMIT_DELAY)


# =========================
# Writer
# =========================
async def writer(write_queue, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        finished = 0

        while True:
            item = await write_queue.get()

            if item is None:
                finished += 1
                write_queue.task_done()
                if finished == NUM_WORKERS:
                    break
                continue

            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            write_queue.task_done()


# =========================
# Image Worker
# =========================
async def image_worker(image_queue):
    async with httpx.AsyncClient(headers=HEADERS, timeout=TIME_OUT) as client:
        while True:
            item = await image_queue.get()

            if item is None:
                image_queue.task_done()
                break

            type_, data = item

            try:
                if type_ == "poster":
                    save_dir = BASE_STATIC_DIR / data["type"]
                    await download_single_image(client, data["path"], save_dir, 
                                                data["id"])

                elif type_ == "cast":
                    save_dir = BASE_STATIC_DIR / "cast"
                    await download_single_cast_image(client, data, save_dir)

            except Exception as e:
                print("Image error:", e)

            image_queue.task_done()


# =========================
# Pipeline runner
# =========================
async def run_pipeline(entity):
    id_queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)
    write_queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)
    image_queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)

    endpoints = (
        ["movie/popular", "movie/top_rated", "movie/upcoming"]
        if entity == "movie"
        else ["tv/popular", "tv/top_rated", "tv/on_the_air"]
    )

    output = MOVIE_OUT if entity == "movie" else TV_OUT

    producer_task = asyncio.create_task(produce_ids(id_queue, endpoints))

    workers = [
        asyncio.create_task(worker(entity, id_queue, write_queue, image_queue))
        for _ in range(NUM_WORKERS)
    ]

    writer_task = asyncio.create_task(writer(write_queue, output))

    image_workers = [
        asyncio.create_task(image_worker(image_queue))
        for _ in range(NUM_IMAGE_WORKERS)
    ]

    await producer_task
    await id_queue.join()

    await asyncio.gather(*workers)
    await write_queue.join()

    # stop image workers
    for _ in range(NUM_IMAGE_WORKERS):
        await image_queue.put(None)

    await image_queue.join()
    await asyncio.gather(*image_workers)

    await writer_task


# =========================
# Main
# =========================
async def main():
    await asyncio.gather(
        run_pipeline("movie"),
        run_pipeline("tv")
    )


if __name__ == "__main__":
    asyncio.run(main())
    