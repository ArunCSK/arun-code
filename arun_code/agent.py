"""Minimal agent tool execution engine.

Provides a registry of local tools that the assistant can invoke
when operating in agent mode. Currently exposes basic file and
shell tools; more can be registered as needed.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass


@dataclass
class ToolResult:
    """Result of a tool invocation."""

    name: str
    output: str
    success: bool


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def read_file(path: str) -> ToolResult:
    """Read and return the contents of a file."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        return ToolResult(name="read_file", output=content, success=True)
    except FileNotFoundError:
        return ToolResult(name="read_file", output=f"File not found: {path}", success=False)
    except OSError as exc:
        return ToolResult(name="read_file", output=str(exc), success=False)


def list_directory(path: str = ".") -> ToolResult:
    """List files and directories at the given path."""
    try:
        entries = os.listdir(path)
        return ToolResult(name="list_directory", output="\n".join(sorted(entries)), success=True)
    except OSError as exc:
        return ToolResult(name="list_directory", output=str(exc), success=False)


def run_shell(command: str) -> ToolResult:
    """Run a shell command and return its stdout/stderr."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        output = result.stdout
        if result.returncode != 0:
            output += f"\n[stderr] {result.stderr}" if result.stderr else ""
        return ToolResult(name="run_shell", output=output, success=result.returncode == 0)
    except subprocess.TimeoutExpired:
        return ToolResult(name="run_shell", output="Command timed out (30s limit)", success=False)


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOLS: dict[str, callable] = {
    "read_file": read_file,
    "list_directory": list_directory,
    "run_shell": run_shell,
}


def execute_tool(name: str, **kwargs) -> ToolResult:
    """Execute a registered tool by name. Returns an error ToolResult if unknown."""
    tool_fn = TOOLS.get(name)
    if tool_fn is None:
        return ToolResult(name=name, output=f"Unknown tool: {name}", success=False)
    return tool_fn(**kwargs)
