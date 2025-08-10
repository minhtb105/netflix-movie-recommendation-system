import os
import logging
from src.base_client import TMDBBaseClient
from utils.downloader import download_image

class CollectionService(TMDBBaseClient):
    async def get_collection_details(self, collection_id: int, language: str = "en-US"):
        """
        Get collection details by ID.
        """
        endpoint = f"/collection/{collection_id}"
        params = {"language": language}
        
        return await self._get(endpoint, params)

    async def get_collection_images(self, collection_id: int):
        """
        Get the images that belong to a collection.
        """
        endpoint = f"/collection/{collection_id}/images"
        params = {"include_image_language": "en,null"}
        
        return await self._get(endpoint, params)

    def collect_images_for_collection(self, collection_id: int, save_dir: str):
        data = self.get_collection_images(collection_id)
        if not data:
            logging.warning(f"No image data found for collection ID: {collection_id}")
            return

        save_dir = os.path.join(save_dir, str(collection_id))
        os.makedirs(save_dir, exist_ok=True)

        for img in data.get('backdrops', []) + data.get('posters', []):
            download_image(img.get('file_path'), save_dir)
