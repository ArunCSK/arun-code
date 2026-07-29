# Quickstart Guide: Arun-Code Local Coding Assistant

## Setup & Installation

1. Ensure Python 3.11+ and `uv` are installed.
2. Clone repository:
   ```bash
   git clone https://github.com/ArunCSK/arun-code.git
   cd arun-code
   ```
3. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Configuration

Set environment variables in `.env`:
```env
NVIDIA_BEARER=your_nvidia_nim_api_key_here
NVIDIA_MODEL=google/diffusiongemma-26b-a4b-it
```

## Running Arun-Code

### CLI Mode
```bash
uv run python -m arun_code.main "Write a python function to compute fibonacci numbers"
```

### Server Mode (for IDE plugins)
```bash
uv run python -m arun_code.server
```
The server will run at `http://localhost:8000`.
