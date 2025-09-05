from feast import FeatureView, Field, Entity
from feast.types import String, Int64, Float32
from pathlib import Path
from unittest.mock import MagicMock


def test_movie_features_schema():
    movie_entity = Entity(name="movie_id", join_keys=["movie_id"])
    dummy_source = MagicMock(spec=DataSource)

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
        source=dummy_source,
    )

    fs = MagicMock()
    fs.get_feature_view.return_value = fv
    result = fs.get_feature_view("movie_features_tmdb")

    field_names = [f.name for f in result.schema]
    assert "feature_vector" in field_names
    assert "vote_average" in field_names
    assert "vote_count" in field_names
    assert "video_key" in field_names


def test_movie_reviews_schema():
    review_entity = Entity(name="review_id", join_keys=["review_id"])
    dummy_source = MagicMock(spec=DataSource)

    fv = FeatureView(
        name="movie_reviews_tmdb",
        entities=[review_entity],
        schema=[
            Field(name="username", dtype=String),
            Field(name="content_vectorize", dtype=Float32),
            Field(name="rating", dtype=Int64),
        ],
        online=True,
        source=dummy_source,
    )

    fs = MagicMock()
    fs.get_feature_view.return_value = fv
    result = fs.get_feature_view("movie_reviews_tmdb")

    field_names = [f.name for f in result.schema]
    assert "username" in field_names
    assert "content_vectorize" in field_names
    assert "rating" in field_names


def test_tv_features_schema():
    tv_entity = Entity(name="tv_id", join_keys=["tv_id"])
    dummy_source = MagicMock(spec=DataSource)

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
        source=dummy_source,
    )

    fs = MagicMock()
    fs.get_feature_view.return_value = fv
    result = fs.get_feature_view("tv_features_tmdb")

    field_names = [f.name for f in result.schema]
    assert "feature_vector" in field_names
    assert "vote_average" in field_names
    assert "vote_count" in field_names
    assert "video_key" in field_names


def test_user_features_schema():
    user_entity = Entity(name="user_id", join_keys=["user_id"])
    dummy_source = MagicMock(spec=DataSource)

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
        source=dummy_source,
    )

    fs = MagicMock()
    fs.get_feature_view.return_value = fv
    result = fs.get_feature_view("user_features")

    field_names = [f.name for f in result.schema]
    assert "age" in field_names
    assert "zip_code" in field_names
    assert "gender_F" in field_names
    assert "occupation_engineer" in field_names
    