"""Unit tests for arun_code.config."""


import pytest

from arun_code.config import load_config


@pytest.fixture(autouse=True)
def _no_dotenv_file(monkeypatch):
    """Prevent load_config's internal load_dotenv() from reading a real
    .env file in the working directory. Without this, these tests are only
    correct by accident - they pass in CI (no .env present) but silently
    break for any developer running pytest from a project directory that
    has a real .env with different values, since load_dotenv() repopulates
    env vars that monkeypatch just deleted.
    """
    monkeypatch.setattr("arun_code.config.load_dotenv", lambda *a, **kw: False)


def test_load_config_missing_api_key(monkeypatch):
    """load_config raises ValueError when NVIDIA_BEARER is not set."""
    monkeypatch.delenv("NVIDIA_BEARER", raising=False)
    with pytest.raises(ValueError, match="NVIDIA_BEARER"):
        load_config()


def test_load_config_with_defaults(monkeypatch):
    """load_config returns sensible defaults when only NVIDIA_BEARER is set."""
    monkeypatch.setenv("NVIDIA_BEARER", "test-key-123")
    # Clear optional vars so defaults apply
    for var in (
        "NVIDIA_ENDPOINT",
        "NVIDIA_MODEL",
        "NVIDIA_AGENT_MODEL",
        "NVIDIA_MAX_TOKENS",
        "NVIDIA_TEMPERATURE",
    ):
        monkeypatch.delenv(var, raising=False)

    config = load_config()

    assert config.api_key == "test-key-123"
    assert "integrate.api.nvidia.com" in config.endpoint
    assert config.model == "google/diffusiongemma-26b-a4b-it"
    assert config.agent_model == "meta/llama-3.1-70b-instruct"
    assert config.max_tokens == 4096
    assert config.temperature == 0.7


def test_load_config_custom_values(monkeypatch):
    """load_config reads custom values from environment."""
    monkeypatch.setenv("NVIDIA_BEARER", "custom-key")
    monkeypatch.setenv("NVIDIA_ENDPOINT", "https://custom.endpoint/v1/chat/completions")
    monkeypatch.setenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")
    monkeypatch.setenv("NVIDIA_AGENT_MODEL", "meta/llama-3.3-70b-instruct")
    monkeypatch.setenv("NVIDIA_MAX_TOKENS", "2048")
    monkeypatch.setenv("NVIDIA_TEMPERATURE", "0.5")

    config = load_config()

    assert config.api_key == "custom-key"
    assert config.endpoint == "https://custom.endpoint/v1/chat/completions"
    assert config.model == "meta/llama-3.1-70b-instruct"
    assert config.agent_model == "meta/llama-3.3-70b-instruct"
    assert config.max_tokens == 2048
    assert config.temperature == 0.5


def test_load_config_agent_model_falls_back_to_chat_model(monkeypatch):
    """If NVIDIA_AGENT_MODEL is unset, agent_model falls back to NVIDIA_MODEL."""
    monkeypatch.setenv("NVIDIA_BEARER", "test-key")
    monkeypatch.setenv("NVIDIA_MODEL", "some/chat-model")
    monkeypatch.delenv("NVIDIA_AGENT_MODEL", raising=False)

    config = load_config()

    assert config.agent_model == "some/chat-model"
