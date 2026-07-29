"""CLI entry point for Arun-Code.

Usage:
    uv run python -m arun_code.main "Your prompt here"
"""

from __future__ import annotations

import sys

from arun_code.config import load_config
from arun_code.errors import format_config_error
from arun_code.models import ChatMessage
from arun_code.nim_client import send_completion


def main() -> None:
    """Send a prompt to NVIDIA NIM and print the response."""
    if len(sys.argv) < 2:
        print("Usage: python -m arun_code.main \"<prompt>\"")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])

    try:
        config = load_config()
    except ValueError as exc:
        print(format_config_error(str(exc)))
        sys.exit(1)

    messages = [ChatMessage(role="user", content=prompt)]
    response = send_completion(messages, config)

    if response.error:
        print(f"Error: {response.error}")
        sys.exit(1)

    if response.reasoning:
        print("--- Reasoning ---")
        print(response.reasoning)
        print()

    print(response.content)


if __name__ == "__main__":
    main()
