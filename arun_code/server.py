"""FastAPI server for Arun-Code.

Exposes an OpenAI-compatible /v1/chat/completions endpoint so that
IDE extensions (VS Code, Antigravity) can communicate with the local
assistant over HTTP.

Run with:
    uv run python -m arun_code.server
"""

from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from arun_code.config import load_config
from arun_code.models import ChatMessage
from arun_code.nim_client import send_completion

app = FastAPI(title="Arun-Code", version="0.1.0")

# Allow all origins so local IDE extensions can connect without CORS issues.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    """Simple health check."""
    return {"status": "ok"}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> JSONResponse:
    """Forward a chat completion request to NVIDIA NIM and return the result."""
    body = await request.json()
    raw_messages = body.get("messages", [])

    if not raw_messages:
        return JSONResponse(
            status_code=400,
            content={"error": {"message": "messages field is required", "type": "invalid_request"}},
        )

    try:
        config = load_config()
    except ValueError as exc:
        return JSONResponse(
            status_code=500,
            content={"error": {"message": str(exc), "type": "configuration_error"}},
        )

    messages = [ChatMessage(role=m["role"], content=m["content"]) for m in raw_messages]
    response = send_completion(messages, config)

    if response.error:
        return JSONResponse(
            status_code=502,
            content={"error": {"message": response.error, "type": "nim_api_error"}},
        )

    return JSONResponse(
        content={
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response.content,
                    }
                }
            ]
        }
    )


def start() -> None:
    """Start the uvicorn server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
