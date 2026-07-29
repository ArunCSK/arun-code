# API Contracts: Local Service Interface

## POST /v1/chat/completions

Standard chat completion interface exposed by the local `arun-code` service for VS Code and Antigravity extension integration.

### Request Body
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Write a Python function to read a file safely."
    }
  ],
  "model": "google/diffusiongemma-26b-a4b-it",
  "stream": false
}
```

### Success Response (200 OK)
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Here is a simple Python function to read a file safely:\n\n..."
      }
    }
  ]
}
```

### Error Response (404 / 500)
```json
{
  "error": {
    "message": "NVIDIA NIM API Error (404): Endpoint or function ID not found. Please verify your NIM function URL and account configuration.",
    "type": "nim_api_error"
  }
}
```
