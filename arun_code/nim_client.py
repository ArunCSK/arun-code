"""NVIDIA NIM HTTP client wrapper.

Handles sending chat completion requests and parsing responses.
Isolates all NIM-specific HTTP logic so the rest of the app stays decoupled.
"""

from __future__ import annotations

import httpx

from arun_code.config import NIMConfig
from arun_code.errors import format_nim_error
from arun_code.models import AgentResponse, ChatMessage


def build_payload(
    messages: list[ChatMessage],
    config: NIMConfig,
    *,
    stream: bool = False,
) -> dict:
    """Build the JSON payload for the NIM chat completions endpoint."""
    return {
        "messages": [{"role": m.role, "content": m.content} for m in messages],
        "model": config.model,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "stream": stream,
    }


def send_completion(
    messages: list[ChatMessage],
    config: NIMConfig,
) -> AgentResponse:
    """Send a non-streaming chat completion request to NVIDIA NIM.

    Returns an AgentResponse with the assistant's reply or an error message.
    """
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Accept": "application/json",
    }
    payload = build_payload(messages, config, stream=False)

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
        content=message.get("content", ""),
        reasoning=message.get("reasoning"),
    )


def _extract_detail(resp: httpx.Response) -> str:
    """Pull a human-readable detail string from an error response."""
    try:
        body = resp.json()
        return body.get("detail", body.get("title", resp.text[:200]))
    except (ValueError, KeyError):
        return resp.text[:200]
