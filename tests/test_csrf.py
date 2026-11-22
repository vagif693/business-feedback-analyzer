import re

import pytest

from src.app import app as flask_app


@pytest.fixture
def csrf_client(tmp_path):
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=True, UPLOAD_FOLDER=str(tmp_path / "uploads"))
    yield flask_app.test_client()
    flask_app.config.update(WTF_CSRF_ENABLED=False)


def get_token(client):
    page = client.get("/").get_data(as_text=True)
    match = re.search(r'name="csrf_token" value="([^"]+)"', page)
    assert match, "CSRF token missing from the page"
    return match.group(1)


def test_post_without_token_is_rejected(csrf_client):
    response = csrf_client.post("/", data={"send_message": "true", "user_message": "hi"})
    assert response.status_code == 400


def test_post_with_wrong_token_is_rejected(csrf_client):
    get_token(csrf_client)
    response = csrf_client.post("/", data={"send_message": "true", "user_message": "hi", "csrf_token": "forged"})
    assert response.status_code == 400


def test_post_with_valid_token_is_accepted(csrf_client):
    token = get_token(csrf_client)
    response = csrf_client.post("/", data={"send_message": "true", "user_message": "hi", "csrf_token": token})
    assert response.status_code == 200
