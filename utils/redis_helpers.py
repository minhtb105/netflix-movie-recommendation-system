import redis
import json

def save_features_to_redis(file_path, prefix, redis_host="localhost", redis_port=6379):
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    with open(file_path, encoding="utf-8") as f:
        features = json.load(f)

    pipe = r.pipeline()
    for item in features:
        _id = item["id"]
        key = f"{prefix}:{_id}"
        pipe.set(key, json.dumps(item, ensure_ascii=False))
    pipe.execute()

    print(f"Saved {len(features)} items to Redis with prefix '{prefix}'")
    
if __name__ == "__main__":
    save_features_to_redis(
        file_path="data/raw/movies_features.json",
        prefix="movie_id",
    )
    
    save_features_to_redis(
        file_path="data/raw/tv_features.json",
        prefix="tv_id",
    )
    
    save_features_to_redis(
        file_path="data/raw/movie_cast_metadata.json",
        prefix="movie_id"
    )
    
    save_features_to_redis(
        file_path="data/raw/tv_cast_metadata.json",
        prefix="tv_id"
    )
    