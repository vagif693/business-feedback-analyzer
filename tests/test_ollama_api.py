import src.ollama_api as ollama_api


class FakeResponse:
    def __init__(self, lines):
        self._lines = lines

    def raise_for_status(self):
        pass

    def iter_lines(self, decode_unicode=True):
        return iter(self._lines)


def test_request_always_has_a_timeout(monkeypatch):
    seen = {}

    def fake_post(url, **kwargs):
        seen.update(kwargs)
        return FakeResponse(['{"response": "ok"}'])

    monkeypatch.setattr(ollama_api.requests, "post", fake_post)
    ollama_api.ask_ollama("hello")
    assert seen.get("timeout") == (ollama_api.CONNECT_TIMEOUT, ollama_api.READ_TIMEOUT)


def test_malformed_lines_are_skipped(monkeypatch):
    lines = ['{"response": "Hello"}', "not json", "", '{"response": " world"}']
    monkeypatch.setattr(ollama_api.requests, "post", lambda url, **kw: FakeResponse(lines))
    assert ollama_api.ask_ollama("hi") == "Hello world"
