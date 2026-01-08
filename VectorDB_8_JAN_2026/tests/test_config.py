import pytest
import importlib

def test_config_loads_without_env(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("CHROMA_PERSIST_DIR", raising=False)

    import app.config

    assert app.config.CHROMA_PERSIST_DIR is not None

