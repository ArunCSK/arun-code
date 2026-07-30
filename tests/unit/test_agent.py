"""Unit tests for arun_code.agent."""

from __future__ import annotations

import os

from arun_code.agent import TOOL_SCHEMAS, TOOLS, edit_file, execute_tool, read_file, write_file


def test_write_file_creates_new_file(tmp_path):
    target = tmp_path / "sub" / "hello.py"
    result = write_file(str(target), "print('hi')\n")

    assert result.success
    assert target.read_text() == "print('hi')\n"


def test_write_file_overwrites_existing(tmp_path):
    target = tmp_path / "hello.py"
    target.write_text("old content")

    result = write_file(str(target), "new content")

    assert result.success
    assert target.read_text() == "new content"


def test_edit_file_replaces_unique_match(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("def foo():\n    return 1\n")

    result = edit_file(str(target), "return 1", "return 2")

    assert result.success
    assert target.read_text() == "def foo():\n    return 2\n"


def test_edit_file_fails_when_snippet_missing(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("def foo():\n    return 1\n")

    result = edit_file(str(target), "return 99", "return 2")

    assert not result.success
    assert "not found" in result.output


def test_edit_file_fails_when_snippet_ambiguous(tmp_path):
    target = tmp_path / "app.py"
    target.write_text("x = 1\nx = 1\n")

    result = edit_file(str(target), "x = 1", "x = 2")

    assert not result.success
    assert "appears 2 times" in result.output


def test_edit_file_missing_file(tmp_path):
    target = tmp_path / "missing.py"

    result = edit_file(str(target), "a", "b")

    assert not result.success
    assert "not found" in result.output


def test_read_file_roundtrip(tmp_path):
    target = tmp_path / "data.txt"
    target.write_text("hello world")

    result = read_file(str(target))

    assert result.success
    assert result.output == "hello world"


def test_execute_tool_dispatches_to_registered_tool(tmp_path):
    target = tmp_path / "out.txt"

    result = execute_tool("write_file", path=str(target), content="via registry")

    assert result.success
    assert target.read_text() == "via registry"


def test_execute_tool_unknown_tool_returns_error():
    result = execute_tool("does_not_exist", foo="bar")

    assert not result.success
    assert "Unknown tool" in result.output


def test_execute_tool_invalid_args_returns_error():
    result = execute_tool("read_file")  # missing required 'path'

    assert not result.success
    assert "Invalid arguments" in result.output


def test_all_registered_tools_have_schemas():
    schema_names = {s["function"]["name"] for s in TOOL_SCHEMAS}
    assert schema_names == set(TOOLS.keys())


def test_tool_schemas_are_valid_openai_function_format():
    for schema in TOOL_SCHEMAS:
        assert schema["type"] == "function"
        fn = schema["function"]
        assert "name" in fn
        assert "description" in fn
        assert fn["parameters"]["type"] == "object"
