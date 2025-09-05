from feast import Entity, FeatureView, Field, FeatureStore, FileSource
from feast.types import Float32, Array, Int32, String, Int64
from feast import ValueType
import os


movie_source = FileSource(
    path=os.path.join(os.path.dirname(__file__).parent[2], "data/feature/movies_tmdb/features"),
    event_timestamp_column='event_timestamp')

movie_id = Entity(name='id', join_keys=['id'], value_type=ValueType.INT64)

movie_features_view = FeatureView(
    name="movie_features_tmdb",
    entities=[movie_id],
    ttl=None,
    schema=[
        Field(name="feature_vector", dtype=Array(Float32), vector_index=True, vector_search_metric="COSINE"),
        Field(name="vote_average", dtype=Float32),  
        Field(name="vote_count", dtype=Int32),
        Field(name="video_key", dtype=String)
    ],
    online=True,
    source=movie_source,
)

store_path_2901 = os.path.join(os.path.dirname(__file__), "store_2901")
os.makedirs(store_path_2901, exist_ok=True)
fs_2901 = FeatureStore(repo_path=store_path_2901)

review_source = FileSource(
    path=os.path.join(os.path.dirname(__file__).parent[2], "data/feature/movies_tmdb/reviews"),
    event_timestamp_column='event_timestamp')

review_id = Entity(name='id', join_keys=['id'], value_type=ValueType.INT64)

movie_reviews_view = FeatureView(
    name="movie_reviews_tmdb",
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

store_path_384 = os.path.join(os.path.dirname(__file__), "store_384")
os.makedirs(store_path_384, exist_ok=True)
fs_384 = FeatureStore(repo_path=store_path_384)

if __name__ == "__main__":
    fs_2901.apply([movie_id, movie_features_view])
    fs_384.apply([review_id, movie_reviews_view])
