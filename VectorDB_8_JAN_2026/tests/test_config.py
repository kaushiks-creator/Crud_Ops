import pytest
import importlib

def test_missing_env(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("CHROMA_PERSIST_DIR", raising=False)

    with pytest.raises(RuntimeError):
        importlib.reload(__import__("app.config"))
