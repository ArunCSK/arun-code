"""NVIDIA NIM HTTP client wrapper.

Handles sending chat completion requests and parsing responses.
Isolates all NIM-specific HTTP logic so the rest of the app stays decoupled.
"""

from __future__ import annotations

import httpx

from arun_code.config import NIMConfig
from arun_code.errors import format_nim_error
from arun_code.models import AgentResponse, ChatMessage


def _serialize_message(m: ChatMessage) -> dict:
    """Convert a ChatMessage into the wire format NIM expects.

    Tool-call fields are only included when present so plain chat requests
    stay identical to the original payload shape.
    """
    msg: dict = {"role": m.role, "content": m.content}
    if m.tool_calls:
        msg["tool_calls"] = m.tool_calls
    if m.tool_call_id:
        msg["tool_call_id"] = m.tool_call_id
    return msg


def build_payload(
    messages: list[ChatMessage],
    config: NIMConfig,
    *,
    stream: bool = False,
    tools: list[dict] | None = None,
    model: str | None = None,
) -> dict:
    """Build the JSON payload for the NIM chat completions endpoint.

    `tools` (OpenAI-style function schemas) and `model` are optional
    overrides used by agent mode; omitted entirely for plain chat requests
    so the payload shape is unchanged from before.
    """
    payload = {
        "messages": [_serialize_message(m) for m in messages],
        "model": model or config.model,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "stream": stream,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
        # Some NIM models (e.g. meta/llama-3.1-70b-instruct) accept a
        # multi-call response but then reject that same message when it's
        # echoed back on the next turn ("only supports single tool-calls at
        # once"). Ask the API not to bundle calls in the first place. loop.py
        # also caps at one call per turn as a defensive backstop in case a
        # model ignores this flag.
        payload["parallel_tool_calls"] = False
    return payload


def send_completion(
    messages: list[ChatMessage],
    config: NIMConfig,
    *,
    tools: list[dict] | None = None,
    model: str | None = None,
) -> AgentResponse:
    """Send a non-streaming chat completion request to NVIDIA NIM.

    Pass `tools` (OpenAI-style function schemas) to enable agent mode; the
    returned AgentResponse.tool_calls will be populated if the model wants
    to invoke one. Pass `model` to override config.model for this call
    (used to route agent-mode requests to a tool-calling-capable model).

    Returns an AgentResponse with the assistant's reply or an error message.
    """
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Accept": "application/json",
    }
    payload = build_payload(messages, config, stream=False, tools=tools, model=model)

    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(config.endpoint, headers=headers, json=payload)
    except httpx.ConnectError:
        return AgentResponse(
            content="",
            error=(
                "Unable to reach the NVIDIA NIM endpoint. "
                "Please check your network connection and NVIDIA_ENDPOINT value."
            ),
        )
    except httpx.TimeoutException:
        return AgentResponse(
            content="",
            error="Request to NVIDIA NIM timed out. Try again or increase the timeout.",
        )

    if resp.status_code >= 400:
        detail = _extract_detail(resp)
        return AgentResponse(
            content="",
            error=format_nim_error(resp.status_code, detail),
        )

    data = resp.json()
    choices = data.get("choices", [])
    if not choices:
        return AgentResponse(content="", error="No choices returned by the model.")

    message = choices[0].get("message", {})
    return AgentResponse(
        content=message.get("content") or "",
        reasoning=message.get("reasoning"),
        tool_calls=message.get("tool_calls") or None,
        finish_reason=choices[0].get("finish_reason"),
    )


def _extract_detail(resp: httpx.Response) -> str:
    """Pull a human-readable detail string from an error response."""
    try:
        body = resp.json()
        return body.get("detail", body.get("title", resp.text[:200]))
    except (ValueError, KeyError):
        return resp.text[:200]
