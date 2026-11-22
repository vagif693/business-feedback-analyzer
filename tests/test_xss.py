import src.app as app_module

PAYLOAD = "<script>alert('xss')</script>"


def start_chat(client):
    with client.session_transaction() as sess:
        sess["uploaded"] = True
        sess["file_text"] = "sample feedback"
        sess["chat_history"] = []


def send(client, message):
    return client.post("/", data={"send_message": "true", "user_message": message})


def test_user_message_is_escaped(client, monkeypatch):
    monkeypatch.setattr(app_module, "ask_ollama", lambda prompt: "ok")
    start_chat(client)
    response = send(client, PAYLOAD)
    assert PAYLOAD.encode() not in response.data
    assert b"&lt;script&gt;" in response.data


def test_ai_response_is_escaped(client, monkeypatch):
    evil = '<img src=x onerror="alert(1)">'
    monkeypatch.setattr(app_module, "ask_ollama", lambda prompt: evil)
    start_chat(client)
    response = send(client, "summarise the feedback")
    assert evil.encode() not in response.data
    assert b"&lt;img" in response.data
