"""Agent-mode orchestration loop.

Wires arun_code.agent's tool registry into arun_code.nim_client's
tool-calling support: sends the task and available tools to NIM, executes
whatever tool calls come back, feeds the results into the conversation, and
repeats until the model responds with plain text (done) or a step limit is
reached. This is what powers `ac agent "<task>"`.
"""

from __future__ import annotations

import json
from collections.abc import Callable

from arun_code.agent import TOOL_SCHEMAS, execute_tool
from arun_code.config import NIMConfig
from arun_code.models import AgentResponse, ChatMessage
from arun_code.nim_client import send_completion

SYSTEM_PROMPT = """You are an autonomous coding agent working inside a project directory.
You have tools to read, write, and edit files, list directories, and run shell commands.

Workflow for every task:
1. Explore first: list_directory and read_file on anything relevant before writing code.
2. Make the smallest correct change using edit_file where possible; use write_file for
   new files or full rewrites.
3. After changing code, RUN it (run_shell) - execute the script, or run the test suite
   if one exists.
4. If a command fails or a test fails, read the error carefully, fix the code, and
   re-run. Repeat until it passes.
5. Do not claim a task is complete without having actually run and verified the code.
6. When truly done, reply with plain text (no tool call) summarizing what changed and
   how it was verified.

Be concise. Prefer idiomatic Python or TypeScript. Write tests for non-trivial logic
when none exist yet.
"""

DEFAULT_MAX_STEPS = 25


def run_agent_task(
    task: str,
    config: NIMConfig,
    *,
    max_steps: int = DEFAULT_MAX_STEPS,
    on_step: Callable[[str], None] | None = None,
) -> AgentResponse:
    """Run an agentic task to completion (or until max_steps is hit).

    `on_step` is an optional callback invoked with a short progress string
    for each tool call, e.g. for CLI output. Returns the final AgentResponse
    - its `.content` is the model's closing summary, `.error` is set if the
    NIM request itself failed at any point.
    """
    messages: list[ChatMessage] = [
        ChatMessage(role="system", content=SYSTEM_PROMPT),
        ChatMessage(role="user", content=task),
    ]

    for _ in range(max_steps):
        response = send_completion(
            messages,
            config,
            tools=TOOL_SCHEMAS,
            model=config.agent_model,
        )

        if response.error:
            return response

        if not response.tool_calls:
            # No more tool calls requested - the agent considers itself done.
            messages.append(ChatMessage(role="assistant", content=response.content))
            return response

        tool_calls = response.tool_calls
        if len(tool_calls) > 1:
            # This model (or this response) bundled multiple calls into one
            # turn. Some NIM models accept that on the way out but then
            # reject the same message being echoed back on the next
            # round-trip ("only supports single tool-calls at once"). Keep
            # only the first call; the model will naturally ask for the
            # next one once it sees this turn's result.
            if on_step:
                dropped = ", ".join(c.get("function", {}).get("name", "?") for c in tool_calls[1:])
                on_step(f"(model requested {len(tool_calls)} calls at once; running 1, deferring: {dropped})")
            tool_calls = tool_calls[:1]

        messages.append(
            ChatMessage(
                role="assistant",
                content=response.content or "",
                tool_calls=tool_calls,
            )
        )

        for call in tool_calls:
            fn = call.get("function", {})
            name = fn.get("name", "")
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}

            if on_step:
                on_step(f"{name}({args})")

            result = execute_tool(name, **args)

            if on_step:
                preview = result.output[:200].replace("\n", " ")
                on_step(f"  -> {'ok' if result.success else 'ERROR'}: {preview}")

            messages.append(
                ChatMessage(
                    role="tool",
                    content=result.output,
                    tool_call_id=call.get("id", ""),
                )
            )

    return AgentResponse(
        content="",
        error=f"Agent stopped after {max_steps} steps without finishing. "
        "Try raising --max-steps or narrowing the task.",
    )
