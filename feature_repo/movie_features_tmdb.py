from feast import Entity, FeatureView, Field, FeatureStore, FileSource, FeatureStore
from feast import ValueType
from feast.types import Float32, Array, Int32, String, Int64
import os


movie_source = FileSource(
    path=os.path.join(os.path.dirname(__file__), "data/movies_tmdb/movie_features_train.parquet"),
    event_timestamp_column='event_timestamp')

movie_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

movie_features_view = FeatureView(
    name="movie_features_tmdb",
    entities=[movie_id],
    ttl=None,
    schema=[
        Field(name="feature_vector", dtype=Array(Float32)),
        Field(name="vote_average", dtype=Float32),
        Field(name="vote_count", dtype=Int32),
        Field(name="video_key", dtype=String)
    ],
    online=True,
    source=movie_source
)

os.makedirs("store_2047", exist_ok=True)
store_path = os.path.join(os.path.dirname(__file__), "store_2047")
fs_2047 = FeatureStore(repo_path=store_path)
fs_2047.apply([movie_id, movie_features_view])

review_source = FileSource(
    path=os.path.join(os.path.dirname(__file__), "data/movies_tmdb/movie_reviews_train.parquet"),
    event_timestamp_column='event_timestamp')

review_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

movie_reviews_view = FeatureView(
    name="movie_reviews_tmdb",
    entities=[review_id],
    ttl=None,
    schema=[
        Field(name="username", dtype=String),
        Field(name="content_vectorize", dtype=Array(Float32)),
        Field(name="rating", dtype=Int64)
    ],
    online=True,
    source=review_source
)

os.makedirs("store_384", exist_ok=True)
store_path = os.path.join(os.path.dirname(__file__), "store_384")
fs_384 = FeatureStore(repo_path=store_path)
fs_384.apply([review_id, movie_reviews_view])

