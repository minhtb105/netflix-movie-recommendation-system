from fastapi import APIRouter, Query
from services.collection_api import CollectionService

router = APIRouter()
service = CollectionService()

@router.get("/collection/{collection_id}")
async def get_collection_details(collection_id: int, language: str = Query("en-US")):
    """
    Get collection details by ID.
    """
    return await service.get_collection_details(collection_id, language)

@router.get("/collection/{collection_id}/images")
async def get_collection_images(collection_id: int):
    """
    Get collection images by ID.
    """
    return await service.get_collection_images(collection_id)
