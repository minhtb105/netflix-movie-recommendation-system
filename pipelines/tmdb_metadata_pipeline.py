from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import json
import asyncio
from utils.downloader import async_batch_download_images, download_cast_images_batch 
from services.movie_api import MovieService
from services.tv_api import TVService

RAW_DIR = Path("data/raw")
FEATURE_DIR = Path("data/raw") 
RAW_DIR.mkdir(parents=True, exist_ok=True)
FEATURE_DIR.mkdir(parents=True, exist_ok=True)


async def fetch_movie_ids(mv_service: MovieService, max_pages: int = 6):
    movie_ids = set()
    for func in [mv_service.fetch_popular, mv_service.fetch_top_rated, mv_service.fetch_upcoming]:
        for page in range(1, max_pages + 1):
            data = await func(page=page)
            if data and "results" in data:
                for movie in data["results"]:
                    movie_ids.add(movie["id"])
                    
            await asyncio.sleep(0.25)
        
    return list(movie_ids)

movie_metadata_path = f"{RAW_DIR}/movies_metadata.json"
async def fetch_movie_metadata(mv_service: MovieService, movie_ids: list[int],
                               out_path: str = movie_metadata_path):
    all_meta = []
    for mid in movie_ids:
        # parallel fetch
        details = await mv_service.fetch_movie_details(mid)
        videos = await mv_service.fetch_trailers(mid)
        reviews = await mv_service.fetch_movie_reviews(mid)
        all_meta.append({
            "id": mid,
            "details": details,
            "videos": videos,
            "reviews": reviews
        })
        await asyncio.sleep(0.25)
        
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_meta, f, ensure_ascii=False, indent=2)
        
    return all_meta


async def fetch_tv_ids(tv_service: TVService, max_pages: int = 6):
    tv_ids = set()
    for func in [tv_service.fetch_popular_tv, tv_service.fetch_top_rated_tv]:
        for page in range(1, max_pages + 1):
            data = await func(page=page)
            if data and "results" in data:
                for tv in data["results"]:
                    tv_ids.add(tv["id"])
            
            await asyncio.sleep(0.25)
            
    return list(tv_ids)

tv_metadata_path = f"{RAW_DIR}/tv_metadata.json"
async def fetch_tv_metadata(tv_service: TVService, tv_ids: list[int],
                            out_path: str = tv_metadata_path):
    all_meta = []
    for tid in tv_ids:
        details = await tv_service.fetch_tv_details(tid)
        videos = await tv_service.fetch_tv_trailers(tid)
        reviews = await tv_service.fetch_tv_reviews(tid)
        all_meta.append({
            "id": tid,
            "details": details,
            "videos": videos,
            "reviews": reviews
        })
        
        await asyncio.sleep(0.25)
        
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_meta, f, ensure_ascii=False, indent=2)
        
    return all_meta


async def main():
    mv_service = MovieService()
    tv_service = TVService()
    
    movie_ids = await fetch_movie_ids(mv_service)
    movies_meta = await fetch_movie_metadata(mv_service, movie_ids)

    movie_image_infos = []
    movie_cast_list = []
    for r in movies_meta:
        if r.get("details"):
            if r["details"].get("poster_path"):
                movie_image_infos.append({
                    "image_path": r["details"]["poster_path"],
                    "movie_id": r["id"],
                })
             
            casts_info = r['details'].get("credits", {}).get("cast", [])
            for c in casts_info:
                character = (c.get("character") or c.get("roles", [{}])[0].get("character") or "").lower()
                if "uncredited" not in character and "voice" not in character:
                    movie_cast_list.append({
                        "id": c.get("id"),
                        "profile_path": c.get("profile_path", ""),
                        "porpularity": c.get("popularity", 0),
                    })
    sorted_movie_cast_list = sorted(movie_cast_list, key=lambda x: x["porpularity"], reverse=True)[:3]
    
    await async_batch_download_images(movie_image_infos, save_dir="app/static/images/movie")
    await download_cast_images_batch(sorted_movie_cast_list)

    tv_ids = await fetch_tv_ids(tv_service)
    tv_meta = await fetch_tv_metadata(tv_service, tv_ids)

    tv_image_infos = []
    tv_cast_list = []
    for r in tv_meta:
        if r.get("details"):
            if r["details"].get("poster_path"):
                tv_image_infos.append({
                    "image_path": r["details"]["poster_path"],
                    "movie_id": r["id"],
                })
                
            casts_info = r['details'].get("aggregate_credits", {}).get("cast", [])
            for c in casts_info:
                character = (c.get("character") or c.get("roles", [{}])[0].get("character") or "").lower()
                if "uncredited" not in character and "voice" not in character:
                    tv_cast_list.append({
                        "id": c.get("id"),
                        "profile_path": c.get("profile_path", ""),
                        "porpularity": c.get("popularity", 0),
                    })
    sorted_tv_cast_list = sorted(tv_cast_list, key=lambda x: x["porpularity"], reverse=True)[:3]
    
    await async_batch_download_images(tv_image_infos, save_dir="app/static/images/tv")
    await download_cast_images_batch(sorted_tv_cast_list)

    await mv_service.close()
    await tv_service.close()
    
if __name__ == "__main__":
    asyncio.run(main())
    