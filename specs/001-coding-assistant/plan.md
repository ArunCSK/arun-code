# Implementation Plan: Arun-Code Local Coding Assistant

**Branch**: `001-coding-assistant` | **Date**: 2026-07-29 | **Spec**: [spec.md](file:///c:/Users/Arun/projects/arun-code/specs/001-coding-assistant/spec.md)
**Input**: Feature specification from `/specs/001-coding-assistant/spec.md`

## Summary

Build the local coding assistant `arun-code` in Python using `uv` for dependency management. The assistant interfaces with NVIDIA NIM API endpoints (based on patterns demonstrated in `example/hello_agent.py`), provides a local server/CLI runner, and supports integration with IDE extensions while strictly adhering to surgical edits and simplicity principles.

## Technical Context

**Language/Version**: Python 3.11+ managed via `uv`  
**Primary Dependencies**: `httpx`, `fastapi`, `uvicorn`, `python-dotenv`  
**Storage**: N/A (Local context/session in-memory)  
**Testing**: `pytest`  
**Target Platform**: Local Windows / Cross-platform workstation  
**Project Type**: CLI & Local Web Service / Agent Backend  
**Performance Goals**: Prompt response stream initialization within 1 second  
**Constraints**: Minimal emojis, clean human-friendly language, strict error handling for NIM 404/auth failures  
**Scale/Scope**: Open-source local development tool (`ArunCSK/arun-code`)  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-First Development**: PASS (spec.md created & verified)
- **Test-Driven Implementation**: PASS (pytest suites included in design phase)
- **Modular Library Architecture**: PASS (modular decoupling between NIM API client, local agent runner, and server API)
- **CI & Automated Verification**: PASS (uv sync + pytest setup)
- **Governance & Guideline Adherence**: PASS (coding-guidlines applied: surgical edits, minimal code, goal-driven execution)

## Project Structure

### Documentation (this feature)

```text
specs/001-coding-assistant/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
```

### Source Code (repository root)

```text
arun_code/
├── __init__.py
├── main.py              # CLI entry point
├── config.py            # Environment / NIM API settings
├── nim_client.py        # NVIDIA NIM API interaction wrapper
├── agent.py             # Agent mode / tool execution engine
└── server.py            # FastAPI service for IDE extensions

tests/
├── unit/
│   ├── test_config.py
│   └── test_nim_client.py
└── integration/
    └── test_server.py
```

**Structure Decision**: Single Python project structure managed via `pyproject.toml` and `uv`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
