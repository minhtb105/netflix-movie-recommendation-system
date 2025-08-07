import redis
import json

def save_features_to_redis(file_path, prefix, 
                           redis_host="localhost", 
                           redis_port=6379,
                           key_field="id"):
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    with open(file_path, encoding="utf-8") as f:
        features = json.load(f)

    pipe = r.pipeline()
    for item in features:
        _id = item[key_field]
        key = f"{prefix}:{_id}"
        pipe.set(key, json.dumps(item, ensure_ascii=False))
        
    pipe.execute()


def get_item_from_redis(redis_client, prefix: str, item_id: int):
    key = f"{prefix}:{item_id}"
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    
    return None
    
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
        prefix="cast_id",
        key_field="cast_id"
    )
    
    save_features_to_redis(
        file_path="data/raw/tv_cast_metadata.json",
        prefix="cast_id",
        key_field="cast_id"
    )
    