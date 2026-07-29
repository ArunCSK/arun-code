"""Unit tests for arun_code.nim_client."""

from unittest.mock import MagicMock, patch

import httpx

from arun_code.config import NIMConfig
from arun_code.models import ChatMessage
from arun_code.nim_client import build_payload, send_completion

TEST_CONFIG = NIMConfig(
    endpoint="https://test.nvidia.com/v1/chat/completions",
    api_key="test-key",
    model="test-model",
    max_tokens=512,
    temperature=0.5,
)


def test_build_payload():
    """build_payload produces the expected JSON structure."""
    messages = [ChatMessage(role="user", content="hello")]
    payload = build_payload(messages, TEST_CONFIG, stream=False)

    assert payload["model"] == "test-model"
    assert payload["max_tokens"] == 512
    assert payload["messages"] == [{"role": "user", "content": "hello"}]
    assert payload["stream"] is False


def test_send_completion_success():
    """send_completion returns content on a 200 response."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "choices": [{"message": {"content": "Hello back", "role": "assistant"}}]
    }

    with patch("arun_code.nim_client.httpx.Client") as mock_client_cls:
        mock_client_cls.return_value.__enter__ = lambda s: s
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client_cls.return_value.post.return_value = mock_resp

        result = send_completion([ChatMessage(role="user", content="hi")], TEST_CONFIG)

    assert result.content == "Hello back"
    assert result.error is None


def test_send_completion_404_error():
    """send_completion returns a friendly error message on 404."""
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.json.return_value = {"detail": "Function not found"}

    with patch("arun_code.nim_client.httpx.Client") as mock_client_cls:
        mock_client_cls.return_value.__enter__ = lambda s: s
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client_cls.return_value.post.return_value = mock_resp

        result = send_completion([ChatMessage(role="user", content="hi")], TEST_CONFIG)

    assert result.error is not None
    assert "404" in result.error
    assert result.content == ""


def test_send_completion_connect_error():
    """send_completion returns a friendly error on connection failure."""
    with patch("arun_code.nim_client.httpx.Client") as mock_client_cls:
        mock_client_cls.return_value.__enter__ = lambda s: s
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_client_cls.return_value.post.side_effect = httpx.ConnectError("refused")

        result = send_completion([ChatMessage(role="user", content="hi")], TEST_CONFIG)

    assert result.error is not None
    assert "network" in result.error.lower() or "reach" in result.error.lower()
