from pydantic import BaseModel
from datetime import datetime
from typing import List

class TMDBFeatureRequest(BaseModel):
    id: int
    feature_vector: List[float]
    vote_average: float
    vote_count: int
    video_key: str
    event_timestamp: datetime
    
class ReviewFeatureRequest(BaseModel):
    id: int
    username: str
    content_vectorize: List[float]
    rating: int
    event_timestamp: datetime
    