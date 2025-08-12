import pytest

def test_import_main():
    try:
        import app 
    except Exception as e:
        pytest.fail(f"Import app module failed: {e}")
