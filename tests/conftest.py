import pytest

from src.app import app as flask_app


@pytest.fixture
def app(tmp_path):
    upload_dir = tmp_path / "uploads"
    flask_app.config.update(TESTING=True, UPLOAD_FOLDER=str(upload_dir))
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
