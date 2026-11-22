import pytest

from src.app import debug_enabled, load_secret_key


def test_missing_secret_key_refuses_to_start(monkeypatch):
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError):
        load_secret_key()


@pytest.mark.parametrize("weak", ["change-me", "supersecret", "short-key"])
def test_placeholder_or_short_key_is_rejected(monkeypatch, weak):
    monkeypatch.setenv("FLASK_SECRET_KEY", weak)
    with pytest.raises(RuntimeError):
        load_secret_key()


def test_strong_key_is_accepted(monkeypatch):
    key = "a" * 64
    monkeypatch.setenv("FLASK_SECRET_KEY", key)
    assert load_secret_key() == key


def test_debug_is_off_by_default(monkeypatch):
    monkeypatch.delenv("FLASK_DEBUG", raising=False)
    assert debug_enabled() is False


@pytest.mark.parametrize("value", ["0", "true", "yes", ""])
def test_debug_needs_explicit_opt_in(monkeypatch, value):
    monkeypatch.setenv("FLASK_DEBUG", value)
    assert debug_enabled() is False


def test_debug_can_be_enabled_explicitly(monkeypatch):
    monkeypatch.setenv("FLASK_DEBUG", "1")
    assert debug_enabled() is True
