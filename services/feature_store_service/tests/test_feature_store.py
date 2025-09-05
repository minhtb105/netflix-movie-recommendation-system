from feast import FeatureStore
from pathlib import Path

# path tới service feature_store
SERVICE_DIR = Path(__file__).resolve().parent.parent

def test_movie_features_schema():
    fs = FeatureStore(repo_path=str(SERVICE_DIR / "store_2901"))
    fv = fs.get_feature_view("movie_features_tmdb")
    field_names = [f.name for f in fv.schema]

    assert "feature_vector" in field_names
    assert "vote_average" in field_names
    assert "vote_count" in field_names
    assert "video_key" in field_names


def test_movie_reviews_schema():
    fs = FeatureStore(repo_path=str(SERVICE_DIR / "store_384"))
    fv = fs.get_feature_view("movie_reviews_tmdb")
    field_names = [f.name for f in fv.schema]

    assert "username" in field_names
    assert "content_vectorize" in field_names
    assert "rating" in field_names


def test_tv_features_schema():
    fs = FeatureStore(repo_path=str(SERVICE_DIR / "store_2094"))
    fv = fs.get_feature_view("tv_features_tmdb")
    field_names = [f.name for f in fv.schema]

    assert "feature_vector" in field_names
    assert "vote_average" in field_names
    assert "vote_count" in field_names
    assert "video_key" in field_names


def test_user_features_schema():
    fs = FeatureStore(repo_path=str(SERVICE_DIR))
    fv = fs.get_feature_view("user_features")
    field_names = [f.name for f in fv.schema]

    assert "age" in field_names
    assert "zip_code" in field_names
    assert "gender_F" in field_names
    assert "occupation_engineer" in field_names
