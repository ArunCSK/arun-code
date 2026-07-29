# Arun-Code VS Code Extension

Minimal VS Code extension scaffold that connects to the local Arun-Code server.

## Setup

1. Ensure the Arun-Code server is running at `http://localhost:8000`.
2. Open this directory in VS Code.
3. Run `npm install`.
4. Press `F5` to launch the extension in a development host.

## How It Works

The extension registers a chat command that sends the user's input to
`POST http://localhost:8000/v1/chat/completions` and displays the
response in an output panel.
