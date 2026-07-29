"""Shared data models for Arun-Code."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    """A single chat message in a conversation."""

    role: str  # "user", "assistant", or "system"
    content: str


@dataclass
class AgentResponse:
    """Response returned by the assistant to the caller."""

    content: str
    reasoning: str | None = None
    tool_calls: list[dict] | None = field(default=None)
    error: str | None = None
