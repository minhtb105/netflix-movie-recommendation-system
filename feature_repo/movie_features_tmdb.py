from feast import Entity, FeatureView, Field, FeatureStore, FileSource
from feast import ValueType
from feast.types import Float32, Array


movie_source = FileSource(
    path='data/movies_tmdb/movie_features_train.parquet',
    event_timestamp_column='event_timestamp')

movie_id = Entity(name='movie_id', 
              join_keys=['movie_id'], 
              value_type=ValueType.INT64)

movie_features_view = FeatureView(
    name="movie_features_tmdb",
    entities=[movie_id],
    ttl=None,
    schema=[
        Field(name="feature_vector", dtype=Array(Float32))
    ],
    source=movie_source
)

review_source = FileSource(
    path='data/movies_tmdb/movie_reviews_train.parquet',
    event_timestamp_column='event_timestamp')

review_id = Entity(name='movie_id', 
              join_keys=['movie_id'], 
              value_type=ValueType.INT64)

movie_reviews_view = FeatureView(
    name="movie_reviews_tmdb",
    entities=[review_id],
    ttl=None,
    schema=[
        Field(name="review_vectorize", dtype=Array(Float32))
    ],
    source=review_source
)
