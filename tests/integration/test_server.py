"""Integration tests for arun_code.server."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from arun_code.models import AgentResponse
from arun_code.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    """GET /health returns 200 with status ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_chat_completions_empty_messages(client):
    """POST /v1/chat/completions with empty messages returns 400."""
    resp = client.post("/v1/chat/completions", json={"messages": []})
    assert resp.status_code == 400
    assert "required" in resp.json()["error"]["message"]


@patch("arun_code.server.send_completion")
@patch("arun_code.server.load_config")
def test_chat_completions_success(mock_config, mock_send, client):
    """POST /v1/chat/completions returns the model response on success."""
    mock_config.return_value = MagicMock()
    mock_send.return_value = AgentResponse(content="Generated code here")

    resp = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "write hello world"}]},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["choices"][0]["message"]["content"] == "Generated code here"


@patch("arun_code.server.send_completion")
@patch("arun_code.server.load_config")
def test_chat_completions_nim_error(mock_config, mock_send, client):
    """POST /v1/chat/completions returns 502 when NIM fails."""
    mock_config.return_value = MagicMock()
    mock_send.return_value = AgentResponse(content="", error="NIM unreachable")

    resp = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "hello"}]},
    )

    assert resp.status_code == 502
    assert "NIM unreachable" in resp.json()["error"]["message"]
