"""CLI entry point for Arun-Code.

Usage:
    uv run python -m arun_code.main "Your prompt here"
    uv run python -m arun_code.main agent "Fix the failing test in tests/unit"
    uv run python -m arun_code.main agent --max-steps 40 "Add a health endpoint"
"""

from __future__ import annotations

import argparse
import os
import sys

from arun_code.config import load_config
from arun_code.errors import format_config_error
from arun_code.loop import DEFAULT_MAX_STEPS, run_agent_task
from arun_code.models import ChatMessage
from arun_code.nim_client import send_completion


def _run_chat(prompt: str) -> None:
    """Original single-turn chat path - unchanged behavior."""
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


def _run_agent(task: str, max_steps: int, workdir: str) -> None:
    """Agent-mode path: runs the tool-calling loop to completion."""
    try:
        config = load_config()
    except ValueError as exc:
        print(format_config_error(str(exc)))
        sys.exit(1)

    original_cwd = os.getcwd()
    if workdir != ".":
        os.makedirs(workdir, exist_ok=True)
        os.chdir(workdir)

    try:
        print(f"[agent] model={config.agent_model} workdir={os.getcwd()}\n")
        response = run_agent_task(
            task,
            config,
            max_steps=max_steps,
            on_step=lambda line: print(f"[agent] {line}"),
        )
    finally:
        os.chdir(original_cwd)

    if response.error:
        print(f"\nError: {response.error}")
        sys.exit(1)

    print(f"\n{response.content}")


def main() -> None:
    """Parse CLI args and dispatch to chat mode or agent mode."""
    if len(sys.argv) < 2:
        print('Usage: python -m arun_code.main "<prompt>"')
        print('   or: python -m arun_code.main agent "<task>" [--workdir DIR] [--max-steps N]')
        sys.exit(1)

    if sys.argv[1] == "agent":
        parser = argparse.ArgumentParser(prog="ac agent")
        parser.add_argument("task", help="Task description for the agent to carry out")
        parser.add_argument(
            "--workdir", default=".", help="Directory the agent may read/write/execute in"
        )
        parser.add_argument(
            "--max-steps",
            type=int,
            default=DEFAULT_MAX_STEPS,
            help="Max tool-call iterations before giving up",
        )
        args = parser.parse_args(sys.argv[2:])
        _run_agent(args.task, args.max_steps, args.workdir)
        return

    prompt = " ".join(sys.argv[1:])
    _run_chat(prompt)


if __name__ == "__main__":
    main()
