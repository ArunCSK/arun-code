"""Shared data models for Arun-Code."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    """A single chat message in a conversation.

    tool_calls / tool_call_id are only populated for agent-mode round-trips:
      - An "assistant" message that requested tool calls carries `tool_calls`
        (the raw OpenAI-style list returned by the model).
      - A "tool" message reporting a tool's result carries `tool_call_id`,
        matching the id the model assigned to that call.
    """

    role: str  # "user", "assistant", "system", or "tool"
    content: str
    tool_calls: list[dict] | None = field(default=None)
    tool_call_id: str | None = field(default=None)


@dataclass
class AgentResponse:
    """Response returned by the assistant to the caller."""

    content: str
    reasoning: str | None = None
    tool_calls: list[dict] | None = field(default=None)
    finish_reason: str | None = field(default=None)
    error: str | None = None
