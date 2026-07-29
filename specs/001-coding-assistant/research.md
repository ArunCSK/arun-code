# Research & Decisions: Arun-Code Local Coding Assistant

## 1. NVIDIA NIM Endpoint Integration & 404 Error Handling

### Decision
Use `httpx` async client to connect to `https://integrate.api.nvidia.com/v1/chat/completions` (or user-configured custom NIM base URLs). Standardize authorization via `NVIDIA_BEARER` or `NVIDIA_API_KEY` environment variables. Catch 404 responses specifically to identify invalid function IDs/accounts and format actionable error guidance.

### Rationale
In `example/hello_agent.py`, requests are dispatches directly via HTTP POST with `Authorization: Bearer <token>`. Known Copilot chat issues trigger 404 when an account function UUID is misconfigured. Intercepting response status code `404` and checking JSON response body allows `arun-code` to produce human-friendly troubleshooting steps without crashing.

### Alternatives Considered
- Direct usage of OpenAI SDK: Useful but adds additional abstraction over standard NIM endpoint responses. `httpx` provides surgical control over request headers, streaming events, and status checks.

---

## 2. Package & Dependency Management with `uv`

### Decision
Initialize standard `pyproject.toml` with `hatchling` or standard setuptools build backend, leveraging `uv` commands (`uv sync`, `uv run`) for environment and script execution.

### Rationale
Aligns strictly with user requirements and project constitution for fast, reproducible dependency management.

---

## 3. IDE Integration & Local HTTP Server

### Decision
Expose a lightweight FastAPI server with `/v1/chat/completions` and `/health` endpoints.

### Rationale
Provides a standard OpenAI-compatible API interface that VS Code, Antigravity, and custom Web interfaces can connect to without custom protocol adapters.
