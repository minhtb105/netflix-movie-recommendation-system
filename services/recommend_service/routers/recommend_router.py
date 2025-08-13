from fastapi import from fastapi import APIRouter, HTTPException
from src.model_loader import ModelLoader
from schemas.recommend_request import RecommendRequest, RecommendResponse


router = APIRouter(prefix="/recommend")

@router.post("/user-based", response_model=RecommendResponse)
def recommend_user_based(req: RecommendRequest):
    model = model_loader.get_user_cf_model()
    if req.user_id is None:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    predictions = model.predict([{"user_id": req.user_id, "item_id": i, "k": req.k} for i in range(1, 1000)])
    ranked = sorted(enumerate(predictions, 1), key=lambda x: (x[1] is not None, x[1]), reverse=True)
    recommended = [item_id for item_id, score in ranked[:req.k]]
    
    return {"recommendations": recommended}

@router.post("/recommend/item-based/", response_model=RecommendResponse)
def recommend_item_based(req: RecommendRequest):
    model = model_loader.get_item_cf_model()
    if req.user_id is None:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    predictions = model.predict([{"user_id": req.user_id, "item_id": i, "k": req.k} for i in range(1, 1000)])
    ranked = sorted(enumerate(predictions, 1), key=lambda x: (x[1] is not None, x[1]), reverse=True)
    recommended = [item_id for item_id, score in ranked[:req.k]]
    
    return {"recommendations": recommended}

@router.post("/recommend/content-based/", response_model=RecommendResponse)
def recommend_content_based(req: RecommendRequest):
    model = model_loader.get_content_based_model()
    if req.movie_id is None:
        raise HTTPException(status_code=400, detail="movie_id is required")
    
    result = model.predict([{"movie_id": req.movie_id}], params={"top_k": req.top_k})
    recommendations = result[0]["recommendations"]
    
    return {"recommendations": recommendations}
