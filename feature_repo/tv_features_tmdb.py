from feast import Entity, FeatureView, Field, FeatureStore, FileSource
from feast import ValueType
from feast.types import Float32, Array, Int32, String


tv_source = FileSource(
    path='data/tv_tmdb/tv_features_train.parquet',
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
    source=tv_source
)

review_source = FileSource(
    path='data/tv_tmdb/tv_reviews_train.parquet',
    event_timestamp_column='event_timestamp')

review_id = Entity(name='id', 
              join_keys=['id'], 
              value_type=ValueType.INT64)

tv_reviews_view = FeatureView(
    name="tv_reviews_tmdb",
    entities=[review_id],
    ttl=None,
    schema=[
        Field(name="review_vectorize", dtype=Array(Float32))
    ],
    source=review_source
)
