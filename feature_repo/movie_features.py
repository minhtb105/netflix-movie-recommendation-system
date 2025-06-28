from datetime import datetime
import pandas as pd
from feast import Entity, FeatureView, Field, FeatureStore
from feast import FileSource
from feast import ValueType
from feast.data_format import ParquetFormat
from feast.types import Float64, Int32, Int64, Array


movie_source = FileSource(
    path=r'data/movies/movie_features_train.parquet',
    event_timestamp_column='release_date')

movie = Entity(name='movie_id', 
              join_keys=['movie_id'], 
              value_type=ValueType.INT64)

movie_fv = FeatureView(
    name="movie_features",
    entities=[movie],
    ttl=None,
    schema=[
        Field(name='unknown', dtype=Int64),
        Field(name='Action', dtype=Int64),
        Field(name='Adventure', dtype=Int64),
        Field(name='Animation', dtype=Int64),
        Field(name="Children", dtype=Int64),
        Field(name='Comedy', dtype=Int64),
        Field(name='Crime', dtype=Int64),
        Field(name='Documentary', dtype=Int64),
        Field(name='Drama', dtype=Int64),
        Field(name='Fantasy', dtype=Int64),
        Field(name='Film_Noir', dtype=Int64),
        Field(name='Horror', dtype=Int64),
        Field(name='Musical', dtype=Int64),
        Field(name='Mystery', dtype=Int64),
        Field(name='Romance', dtype=Int64),
        Field(name='Sci_Fi', dtype=Int64),
        Field(name='Thriller', dtype=Int64),
        Field(name='War', dtype=Int64),
        Field(name='Western', dtype=Int64),
        Field(name='release_date_year', dtype=Float64),
        Field(name='release_date_month', dtype=Float64),
        Field(name='release_date_day', dtype=Float64),
        Field(name='release_date_hour', dtype=Float64),
        Field(name='release_date_daypofweek', dtype=Float64),
        Field(name='release_date_is_weekend', dtype=Int32),
        Field(name='title_tfidf', dtype=Array(Float64)),
    ],
    source=movie_source
)
