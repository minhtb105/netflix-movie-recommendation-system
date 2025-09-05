from feast import FeatureView, Field, Entity, String, Int64, Float32, FeatureStore, DataSource
from pathlib import Path
from unittest.mock import MagicMock


def test_movie_features_schema():
    fs = MagicMock()
    movie_entity = Entity(name="movie_id", join_keys=["movie_id"])
    
    fv = FeatureView(
        name="movie_features_tmdb",
        entities=[movie_entity],
        schema=[
            Field(name="feature_vector", dtype=Float32),
            Field(name="vote_average", dtype=Float32),
            Field(name="vote_count", dtype=Int64),
            Field(name="video_key", dtype=String),
        ],
        online=True,
        source=MagicMock(),
    )
    fs.get_feature_view.return_value = fv

    result = fs.get_feature_view("movie_features_tmdb")

    assert result.name == "movie_features_tmdb"
    assert any(f.name == "feature_vector" for f in result.schema)
    assert any(f.name == "vote_average" for f in result.schema)
    assert any(f.name == "vote_count" for f in result.schema)
    assert any(f.name == "video_key" for f in result.schema)


def test_movie_reviews_schema():
    fs = MagicMock()
    review_entity = Entity(name="review_id", join_keys=["review_id"])
    
    fv = FeatureView(
        name="movie_reviews_tmdb",
        entities=[review_entity],
        schema=[
            Field(name="username", dtype=String),
            Field(name="content_vectorize", dtype=Float32),
            Field(name="rating", dtype=Float32),
        ],
        online=True,
        source=MagicMock(),
    )
    fs.get_feature_view.return_value = fv

    result = fs.get_feature_view("movie_reviews_tmdb")
    field_names = [f.name for f in result.schema]

    assert "username" in field_names
    assert "content_vectorize" in field_names
    assert "rating" in field_names


def test_tv_features_schema():
    fs = MagicMock()
    tv_entity = Entity(name="tv_id", join_keys=["tv_id"])
    
    fv = FeatureView(
        name="tv_features_tmdb",
        entities=[tv_entity],
        schema=[
            Field(name="feature_vector", dtype=Float32),
            Field(name="vote_average", dtype=Float32),
            Field(name="vote_count", dtype=Int64),
            Field(name="video_key", dtype=String),
        ],
        online=True,
        source=MagicMock(),
    )
    fs.get_feature_view.return_value = fv

    result = fs.get_feature_view("tv_features_tmdb")
    field_names = [f.name for f in result.schema]

    assert "feature_vector" in field_names
    assert "vote_average" in field_names
    assert "vote_count" in field_names
    assert "video_key" in field_names


def test_user_features_schema():
    fs = MagicMock()
    user_entity = Entity(name="user_id", join_keys=["user_id"])
    
    fv = FeatureView(
        name="user_features",
        entities=[user_entity],
        schema=[
            Field(name="age", dtype=Int64),
            Field(name="zip_code", dtype=String),
            Field(name="gender_F", dtype=Int64),
            Field(name="occupation_engineer", dtype=Int64),
        ],
        online=True,
        source=MagicMock(),
    )
    fs.get_feature_view.return_value = fv

    result = fs.get_feature_view("user_features")
    field_names = [f.name for f in result.schema]

    assert "age" in field_names
    assert "zip_code" in field_names
    assert "gender_F" in field_names
    assert "occupation_engineer" in field_names
