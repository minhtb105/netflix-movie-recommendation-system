from clients.base_client import TMDBBaseClient

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
