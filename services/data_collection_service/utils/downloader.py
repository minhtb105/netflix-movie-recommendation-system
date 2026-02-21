import os
import asyncio
import aiofiles


BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w300"
MAX_CONCURRENT_DOWNLOADS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)


async def download_single_image(client, image_path: str, save_dir: str, file_id: str):
    if not image_path or not file_id:
        return

    os.makedirs(save_dir, exist_ok=True)

    url = f"{BASE_IMAGE_URL}{image_path}"
    save_path = os.path.join(save_dir, f"{file_id}.jpg")

    # skip if exists
    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        return

    async with semaphore:
        try:
            async with client.stream("GET", url) as response:
                if response.status_code != 200:
                    return

                async with aiofiles.open(save_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        await f.write(chunk)

        except Exception as e:
            print(f"Download error: {e}")
        
async def download_single_cast_image(client, cast: dict, save_dir: str):
    profile_path = cast.get("profile_path")
    cast_id = cast.get("id")

    if not profile_path or not cast_id:
        return

    await download_single_image(client, profile_path, save_dir, str(cast_id))
    