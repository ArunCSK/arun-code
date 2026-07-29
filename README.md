# Arun-Code

A local coding assistant powered by NVIDIA NIM endpoints. Built for developers who want a private, self-hosted AI coding tool that handles code generation, completion, refactoring, and review.

## Features

- **CLI mode** -- Send prompts directly from the terminal and receive human-friendly responses.
- **Local HTTP server** -- FastAPI service at `localhost:8000` compatible with OpenAI-style `/v1/chat/completions` requests.
- **VS Code extension** -- Chat panel that connects to the local server for in-editor assistance.
- **Agent tools** -- File reading, directory listing, and shell execution for agentic workflows.
- **Clear error handling** -- Structured troubleshooting guidance for NVIDIA NIM API failures (404, 401, timeouts).

## Requirements

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/) package manager
- A valid NVIDIA NIM API key ([get one here](https://build.nvidia.com/))

## Installation

```bash
git clone https://github.com/ArunCSK/arun-code.git
cd arun-code
uv sync
```

## Configuration

Copy the example environment file and set your API key:

```bash
cp .env.example .env
```

Edit `.env` and replace `your_nvidia_api_key_here` with your actual NVIDIA NIM API key:

```env
NVIDIA_BEARER=nvapi-xxxxxxxxxxxxxxxxxxxxx
NVIDIA_MODEL=google/diffusiongemma-26b-a4b-it
```

## Usage

### CLI

```bash
uv run python -m arun_code.main "Write a Python function that reads a CSV file"
```

### Server (for IDE extensions)

```bash
uv run python -m arun_code.server
```

The server starts at `http://localhost:8000`. You can test it with:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### VS Code Extension

See [vscode-extension/README.md](vscode-extension/README.md) for setup instructions.

## Running Tests

```bash
uv sync --extra dev
uv run pytest
```

## Project Structure

```
arun_code/
  __init__.py       -- Package metadata
  config.py         -- Environment variable loader
  models.py         -- Shared data models (ChatMessage, AgentResponse)
  nim_client.py     -- NVIDIA NIM HTTP client wrapper
  errors.py         -- Structured error formatting
  agent.py          -- Agent tool execution engine
  main.py           -- CLI entry point
  server.py         -- FastAPI server for IDE integration

tests/
  unit/             -- Unit tests for config and NIM client
  integration/      -- Server endpoint tests

vscode-extension/   -- VS Code extension scaffold
```

## Contributing

Contributions are welcome. Please follow the coding guidelines in `.github/skills/coding-guidlines/SKILL.md`:

1. Think before coding -- surface assumptions and tradeoffs.
2. Simplicity first -- minimum code that solves the problem.
3. Surgical changes -- touch only what you must.
4. Goal-driven execution -- define success criteria and verify.

## License

MIT
