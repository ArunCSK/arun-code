"""Unit tests for arun_code.loop."""

from __future__ import annotations

from unittest.mock import patch

from arun_code.config import NIMConfig
from arun_code.loop import run_agent_task
from arun_code.models import AgentResponse

TEST_CONFIG = NIMConfig(
    endpoint="https://test.nvidia.com/v1/chat/completions",
    api_key="test-key",
    model="test-model",
    agent_model="test-agent-model",
    max_tokens=512,
    temperature=0.5,
)


def test_run_agent_task_finishes_without_tool_calls():
    """If the model never requests a tool, the loop returns immediately."""
    final = AgentResponse(content="Nothing to do here.", tool_calls=None)

    with patch("arun_code.loop.send_completion", return_value=final) as mock_send:
        response = run_agent_task("do nothing", TEST_CONFIG, max_steps=5)

    assert response.content == "Nothing to do here."
    assert mock_send.call_count == 1
    # agent_model must be used, not the default chat model
    assert mock_send.call_args.kwargs["model"] == "test-agent-model"


def test_run_agent_task_executes_tool_then_finishes():
    """One tool call round-trip: write_file, then a final plain-text reply."""
    tool_call_response = AgentResponse(
        content="",
        tool_calls=[
            {
                "id": "call_1",
                "type": "function",
                "function": {
                    "name": "write_file",
                    "arguments": '{"path": "ignored_in_test.txt", "content": "hi"}',
                },
            }
        ],
    )
    final_response = AgentResponse(content="Done, file written.", tool_calls=None)

    with patch("arun_code.loop.send_completion", side_effect=[tool_call_response, final_response]):
        with patch("arun_code.loop.execute_tool") as mock_execute:
            from arun_code.agent import ToolResult

            mock_execute.return_value = ToolResult(name="write_file", output="Wrote 2 chars", success=True)
            response = run_agent_task("write a file", TEST_CONFIG, max_steps=5)

    assert response.content == "Done, file written."
    mock_execute.assert_called_once_with("write_file", path="ignored_in_test.txt", content="hi")


def test_run_agent_task_stops_at_max_steps():
    """If the model keeps requesting tools forever, the loop gives up cleanly."""
    endless_tool_call = AgentResponse(
        content="",
        tool_calls=[
            {
                "id": "call_x",
                "type": "function",
                "function": {"name": "list_directory", "arguments": "{}"},
            }
        ],
    )

    with patch("arun_code.loop.send_completion", return_value=endless_tool_call):
        with patch("arun_code.loop.execute_tool") as mock_execute:
            from arun_code.agent import ToolResult

            mock_execute.return_value = ToolResult(name="list_directory", output="a\nb", success=True)
            response = run_agent_task("loop forever", TEST_CONFIG, max_steps=3)

    assert response.error is not None
    assert "3 steps" in response.error


def test_run_agent_task_propagates_nim_error():
    """A NIM-level error (network, 4xx, etc.) short-circuits the loop."""
    error_response = AgentResponse(content="", error="NVIDIA NIM API error (401): unauthorized")

    with patch("arun_code.loop.send_completion", return_value=error_response):
        response = run_agent_task("do something", TEST_CONFIG, max_steps=5)

    assert response.error == "NVIDIA NIM API error (401): unauthorized"


def test_run_agent_task_calls_on_step_callback():
    tool_call_response = AgentResponse(
        content="",
        tool_calls=[
            {
                "id": "call_1",
                "type": "function",
                "function": {"name": "list_directory", "arguments": "{}"},
            }
        ],
    )
    final_response = AgentResponse(content="done", tool_calls=None)
    steps: list[str] = []

    with patch("arun_code.loop.send_completion", side_effect=[tool_call_response, final_response]):
        with patch("arun_code.loop.execute_tool") as mock_execute:
            from arun_code.agent import ToolResult

            mock_execute.return_value = ToolResult(name="list_directory", output="a\nb", success=True)
            run_agent_task("list stuff", TEST_CONFIG, max_steps=5, on_step=steps.append)

    assert any("list_directory" in s for s in steps)
    assert any("ok:" in s for s in steps)
