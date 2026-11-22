import io
import os


def upload(client, filename, content=b"great service, slow delivery"):
    return client.post(
        "/",
        data={"upload_file": "true", "datafile": (io.BytesIO(content), filename)},
        content_type="multipart/form-data",
    )


def test_normal_upload_works(client):
    response = upload(client, "feedback.txt")
    assert response.status_code == 200
    assert b"File uploaded!" in response.data


def test_path_traversal_cannot_write_outside_upload_dir(app, client, tmp_path):
    response = upload(client, "../../evil.txt", b"pwned")
    assert response.status_code == 200
    assert not (tmp_path / "evil.txt").exists()
    assert not (tmp_path.parent / "evil.txt").exists()


def test_uploaded_file_is_deleted_after_processing(app, client):
    upload(client, "feedback.txt")
    upload_dir = app.config["UPLOAD_FOLDER"]
    assert os.listdir(upload_dir) == []


def test_disallowed_extension_is_rejected(app, client):
    response = upload(client, "shell.py", b"import os")
    assert b"Unsupported file type" in response.data
    assert not os.path.exists(app.config["UPLOAD_FOLDER"]) or os.listdir(app.config["UPLOAD_FOLDER"]) == []


def test_file_without_extension_is_rejected(client):
    response = upload(client, "README")
    assert b"Unsupported file type" in response.data


def test_oversized_upload_is_rejected(client):
    big = b"x" * (5 * 1024 * 1024 + 1)
    response = upload(client, "big.txt", big)
    assert response.status_code == 413
