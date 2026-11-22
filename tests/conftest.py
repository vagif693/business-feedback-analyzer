import os

os.environ.setdefault("FLASK_SECRET_KEY", "test-only-key-0123456789abcdef0123456789")

import pytest

from src.app import app as flask_app


@pytest.fixture
def app(tmp_path):
    upload_dir = tmp_path / "uploads"
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False, UPLOAD_FOLDER=str(upload_dir))
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
