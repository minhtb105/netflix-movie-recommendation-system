from feast import Entity, FeatureView, Field, FeatureStore, FileSource, FeatureStore
from feast import ValueType
from feast.types import Float32, Array, Int32, String
import os


tv_source = FileSource(
    path=os.path.join(os.path.dirname(__file__), "data/tv_tmdb/tv_features_train.parquet"),
    event_timestamp_column='event_timestamp')

series_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

tv_features_view = FeatureView(
    name="tv_features_tmdb",
    entities=[series_id],
    ttl=None,
    schema=[
        Field(name="feature_vector", dtype=Array(Float32)),
        Field(name="vote_average", dtype=Float32),
        Field(name="vote_count", dtype=Int32),
        Field(name="video_key", dtype=String)
    ],
    online=True,
    source=tv_source
)

os.makedirs("store_2664", exist_ok=True)
store_path = os.path.join(os.path.dirname(__file__), "store_2664")
fs_2664 = FeatureStore(repo_path=store_path)
fs_2664.apply([series_id, tv_features_view])

review_source = FileSource(
    path=os.path.join(os.path.dirname(__file__), "data/tv_tmdb/tv_reviews_train.parquet"),
    event_timestamp_column='event_timestamp')

review_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

tv_reviews_view = FeatureView(
    name="tv_reviews_tmdb",
    entities=[review_id],
    ttl=None,
    schema=[
        Field(name="user", dtype=String),
        Field(name="content_vectorize", dtype=Array(Float32)),
        Field(name="rating", dtype=String)
    ],
    online=True,
    source=review_source
)

os.makedirs("store_768", exist_ok=True)
store_path = os.path.join(os.path.dirname(__file__), "store_768")
fs_768 = FeatureStore(repo_path=store_path)
fs_768.apply([review_id, tv_reviews_view])
