from feast import Entity, FeatureView, Field, FeatureStore, FileSource, FeatureStore
from feast import ValueType
from feast.types import Float32, Array, Int32, String, Int64
import os


tv_source = FileSource(
    path=os.path.join(os.path.dirname(__file__).parent[2], "data/feature/tv_tmdb/features"),
    event_timestamp_column='event_timestamp')

series_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

tv_features_view = FeatureView(
    name="tv_features_tmdb",
    entities=[series_id],
    ttl=None,
    schema=[
        Field(name="feature_vector", dtype=Array(Float32), vector_index=True, vector_search_metric="COSINE"),
        Field(name="vote_average", dtype=Float32),
        Field(name="vote_count", dtype=Int32),
        Field(name="video_key", dtype=String)
    ],
    online=True,
    source=tv_source,
)

os.makedirs("store_2094", exist_ok=True)
store_path = os.path.join(os.path.dirname(__file__), "store_2094")
fs_2094 = FeatureStore(repo_path=store_path)


review_source = FileSource(
    path=os.path.join(os.path.dirname(__file__).parent[2], "data/feature/tv_tmdb/reviews"),
    event_timestamp_column='event_timestamp')

review_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

tv_reviews_view = FeatureView(
    name="tv_reviews_tmdb",
    entities=[review_id],
    ttl=None,
    schema=[
        Field(name="username", dtype=String),
        Field(name="content_vectorize", dtype=Array(Float32), vector_index=True, vector_search_metric="COSINE"),
        Field(name="rating", dtype=Int64)
    ],
    online=True,
    source=review_source,
)

os.makedirs("store_384", exist_ok=True)
store_path = os.path.join(os.path.dirname(__file__), "store_384")
fs_384 = FeatureStore(repo_path=store_path)

if __name__ == "__main__":
    fs_2094.apply([series_id, tv_features_view])
    fs_384.apply([review_id, tv_reviews_view])
