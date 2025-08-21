import asyncio
import httpx
from pathlib import Path
import json
import os
from utils.downloader import async_batch_download_images, download_cast_images_batch
from clients.tmdb_service_client import TMDBServiceClient


client = TMDBServiceClient()
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
BASE_STATIC_DIR = Path(
    os.getenv(
        "STATIC_IMAGE_DIR", 
        Path(__file__).resolve().parents[2] / "web_service" / "static" / "images"  # fallback local
    )
)


async def fetch_movie_ids(max_pages=300):
    movie_ids = set()
    for endpoint in ["movie/popular", "movie/top_rated", "movie/upcoming"]:
        for page in range(1, max_pages + 1):
            data = await client._get(endpoint, params={"page": page})
        
            if data and "results" in data:
                movie_ids.update(m["id"] for m in data["results"])
            await asyncio.sleep(0.25)
                
    return list(movie_ids)


async def fetch_movie_metadata(movie_ids, out_path):
    all_meta = []
    for mid in movie_ids:
        details, videos, reviews = await asyncio.gather(
            client._get(f"movie/{mid}"),
            client._get(f"movie/{mid}/videos"),
            client._get(f"movie/{mid}/reviews"),
        )
        all_meta.append({
            "id": mid,
            "details": details.json(),
            "videos": videos.json(),
            "reviews": reviews.json()
        })
        await asyncio.sleep(0.25)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_meta, f, ensure_ascii=False, indent=2)
        
    return all_meta


async def process_movie_images(movies_meta):
    image_infos = []
    cast_list = []
    for r in movies_meta:
        if r.get("details"):
            if r["details"].get("poster_path"):
                image_infos.append({
                    "image_path": r["details"]["poster_path"],
                    "movie_id": r["id"],
                })

            casts_info = r['details'].get("credits", {}).get("cast", [])
            filtered_casts = [
                {
                    "id": c.get("id"),
                    "profile_path": c.get("profile_path", ""),
                    "popularity": c.get("popularity", 0),
                }
                for c in casts_info
                if "uncredited" not in (c.get("character") or "").lower()
                and "voice" not in (c.get("character") or "").lower()
            ]
            sorted_casts = sorted(filtered_casts, key=lambda x: x["popularity"], reverse=True)[:3]
            cast_list.extend(sorted_casts)

    await async_batch_download_images(image_infos, save_dir=BASE_STATIC_DIR / "movie")
    await download_cast_images_batch(cast_list)


async def fetch_tv_ids(max_pages=300):
    tv_ids = set()
    for endpoint in ["tv/popular", "tv/top_rated", "tv/on_the_air"]:
        for page in range(1, max_pages + 1):
            data = await client._get(endpoint, params={"page": page})
            
            if data and "results" in data:
                tv_ids.update(tv["id"] for tv in data["results"])
                
            await asyncio.sleep(0.25)
                
    return list(tv_ids)


async def fetch_tv_metadata(tv_ids, out_path):
    all_meta = []
    for tid in tv_ids:
        details, videos, reviews = await asyncio.gather(
            client._get(f"tv/{tid}"),
            client._get(f"tv/{tid}/videos"),
            client._get(f"tv/{tid}/reviews"),
        )
        all_meta.append({
            "id": tid,
            "details": details.json(),
            "videos": videos.json(),
            "reviews": reviews.json()
        })
        await asyncio.sleep(0.25)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_meta, f, ensure_ascii=False, indent=2)
        
    return all_meta


async def process_tv_images(tv_meta):
    image_infos = []
    cast_list = []
    for r in tv_meta:
        if r.get("details"):
            if r["details"].get("poster_path"):
                image_infos.append({
                    "image_path": r["details"]["poster_path"],
                    "movie_id": r["id"],
                })

            casts_info = r['details'].get("aggregate_credits", {}).get("cast", [])
            filtered_casts = [
                {
                    "id": c.get("id"),
                    "profile_path": c.get("profile_path", ""),
                    "popularity": c.get("popularity", 0),
                }
                for c in casts_info
                if "uncredited" not in (c.get("character") or "").lower()
                and "voice" not in (c.get("character") or "").lower()
            ]
            sorted_casts = sorted(filtered_casts, key=lambda x: x["popularity"], reverse=True)[:3]
            cast_list.extend(sorted_casts)

    await async_batch_download_images(image_infos, save_dir=BASE_STATIC_DIR / "tv")
    await download_cast_images_batch(cast_list)

async def main():
    movie_ids, tv_ids = await asyncio.gather(
        fetch_movie_ids(),
        fetch_tv_ids()
    )

    movies_meta, tv_meta = await asyncio.gather(
        fetch_movie_metadata(movie_ids, RAW_DIR / "movies_metadata.json"),
        fetch_tv_metadata(tv_ids, RAW_DIR / "tv_metadata.json")
    )

    await asyncio.gather(
        process_movie_images(movies_meta),
        process_tv_images(tv_meta)
    )


if __name__ == "__main__":
    asyncio.run(main())
