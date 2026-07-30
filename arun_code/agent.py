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


def write_file(path: str, content: str) -> ToolResult:
    """Create a file or overwrite it entirely with the given content."""
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return ToolResult(name="write_file", output=f"Wrote {len(content)} chars to {path}", success=True)
    except OSError as exc:
        return ToolResult(name="write_file", output=str(exc), success=False)


def edit_file(path: str, old_str: str, new_str: str) -> ToolResult:
    """Replace an exact, unique snippet of text in an existing file.

    Prefer this over write_file for small changes - it fails loudly if
    old_str is missing or ambiguous, instead of silently corrupting a file.
    """
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return ToolResult(name="edit_file", output=f"File not found: {path}", success=False)
    except OSError as exc:
        return ToolResult(name="edit_file", output=str(exc), success=False)

    count = text.count(old_str)
    if count == 0:
        return ToolResult(
            name="edit_file",
            output=f"old_str not found in {path}. No changes made.",
            success=False,
        )
    if count > 1:
        return ToolResult(
            name="edit_file",
            output=(
                f"old_str appears {count} times in {path}; must be unique. "
                "Include more surrounding context and try again."
            ),
            success=False,
        )

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(old_str, new_str, 1))
    except OSError as exc:
        return ToolResult(name="edit_file", output=str(exc), success=False)

    return ToolResult(name="edit_file", output=f"Edited {path}", success=True)


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
    "write_file": write_file,
    "edit_file": edit_file,
    "list_directory": list_directory,
    "run_shell": run_shell,
}


def execute_tool(name: str, **kwargs) -> ToolResult:
    """Execute a registered tool by name. Returns an error ToolResult if unknown."""
    tool_fn = TOOLS.get(name)
    if tool_fn is None:
        return ToolResult(name=name, output=f"Unknown tool: {name}", success=False)
    try:
        return tool_fn(**kwargs)
    except TypeError as exc:
        return ToolResult(name=name, output=f"Invalid arguments for {name}: {exc}", success=False)


# ---------------------------------------------------------------------------
# OpenAI-style function schemas, sent to NIM in the request "tools" field so
# tool-calling-capable models know what's available and how to call it.
# ---------------------------------------------------------------------------

TOOL_SCHEMAS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the full contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path to the file"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Create a file or overwrite it entirely with new content. "
                "Use for new files or full rewrites."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                    "content": {"type": "string", "description": "Full file content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": (
                "Replace an exact, unique snippet of text in an existing file. "
                "Prefer this over write_file for small changes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file"},
                    "old_str": {
                        "type": "string",
                        "description": "Exact text to find; must be unique in the file",
                    },
                    "new_str": {"type": "string", "description": "Text to replace it with"},
                },
                "required": ["path", "old_str", "new_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and directories at a given path (default: current directory).",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Default '.'"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": (
                "Run a shell command and return its stdout/stderr. Use to execute "
                "scripts, run tests, or install dependencies."
            ),
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Shell command to run"}},
                "required": ["command"],
            },
        },
    },
]
