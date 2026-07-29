# Feature Specification: Arun-Code Local Coding Assistant

**Feature Branch**: `001-coding-assistant`  
**Created**: 2026-07-29  
**Status**: Draft  
**Input**: User description: "Build local coding assistant Arun-Code using NVIDIA NIM"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Local Agent Mode Prompting & Execution (Priority: P1)

As a software engineer using local AI tools, I want to send natural language coding prompts (code generation, refactoring, code review, quick prototyping) to Arun-Code running locally so that it seamlessly executes agent actions using local tools and returns human-friendly responses backed by NVIDIA NIM endpoints.

**Why this priority**: Core value of the application; provides full local agent capability with tool access and model interaction.

**Independent Test**: Can be tested via CLI or server API by sending a code generation/refactoring prompt and verifying that tool calls execute correctly and the returned text contains human-friendly instructions without unnecessary emojis.

**Acceptance Scenarios**:

1. **Given** a prompt requesting code generation or refactoring, **When** submitted to Arun-Code, **Then** Arun-Code invokes appropriate local tools (file read/write, code search, execution) in agent mode and returns clear, human-friendly responses.
2. **Given** valid NVIDIA NIM API credentials, **When** a request is dispatched, **Then** Arun-Code streams or receives the response seamlessly without endpoint path/model function 404 errors.

---

### User Story 2 - VS Code & Antigravity IDE Integration (Priority: P2)

As a developer using VS Code or Antigravity, I want a plugin / side-panel interface connected to Arun-Code's local server so that I can chat with the assistant and receive code suggestions directly in my active editor environment.

**Why this priority**: Expands usability into developer IDEs, providing a seamless workflow similar to Copilot or Cursor.

**Independent Test**: Can be tested by starting the local Arun-Code HTTP server and invoking chat suggestions from the IDE extension plugin to verify bi-directional communication.

**Acceptance Scenarios**:

1. **Given** the Arun-Code local server is active, **When** a user initiates a chat session from the IDE extension, **Then** the prompt is sent to `localhost` and response stream is rendered accurately in the IDE UI.

---

### User Story 3 - Graceful NVIDIA NIM Error Handling & Endpoint Fallbacks (Priority: P3)

As a developer, I want clear feedback when NVIDIA NIM endpoint requests fail (e.g. 404 Function Not Found or invalid account function ID) so that I can easily diagnose configuration issues.

**Why this priority**: Resolves known issues where 404 API errors disrupt the user chat experience.

**Independent Test**: Can be tested by supplying an invalid function ID or endpoint URL and verifying that Arun-Code surfaces a clean diagnostic error message instead of crashing.

**Acceptance Scenarios**:

1. **Given** an invalid or mismatched NIM function/model endpoint ID, **When** a request is sent, **Then** Arun-Code catches the 404 response and displays a helpful troubleshooting message explaining account/function URL mismatch.

---

### Edge Cases

- What happens when local network connectivity drops during a streamed NIM request?
- How does the system handle concurrent prompt requests from multiple IDE windows?
- What occurs when `uv` package manager environment is missing dependencies or incorrectly configured?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Arun-Code MUST be built and managed using the `uv` package manager across all Python components.
- **FR-002**: Arun-Code MUST provide a local agent runner capable of invoking filesystem, search, and execution tools in response to user coding instructions.
- **FR-003**: System MUST interface with NVIDIA NIM endpoints for LLM chat completion and code generation using configured model/function endpoints.
- **FR-004**: System MUST expose a local HTTP/REST/WebSocket server enabling IDE extensions (VS Code and Antigravity) to communicate with the local assistant.
- **FR-005**: All output responses MUST maintain clean, human-friendly formatting with minimal use of emojis.
- **FR-006**: System MUST handle NIM API errors (including 404 Not Found / missing function errors) and provide human-readable troubleshooting guidance.

### Key Entities

- **Agent Workspace Context**: Represents active files, project metadata, and tool permissions available to Arun-Code during execution.
- **NIM Configuration Profile**: Contains endpoint base URLs, model/function IDs, and API key credentials.
- **IDE Session**: Represents an active connection from VS Code or Antigravity to the local Arun-Code backend service.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can initialize and launch Arun-Code locally using `uv` in under 2 minutes.
- **SC-002**: 100% of NIM API errors (such as 404 function errors) produce friendly, actionable diagnostic guidance rather than raw stack traces.
- **SC-003**: Code generation and tool execution in agent mode successfully completes P1 user scenarios with 0 unhandled exceptions.
- **SC-004**: IDE extension chat interactions display streamed responses within 1 second of first token generation.

## Assumptions

- Python 3.11+ and `uv` package manager are available on the user's host environment.
- The user has an active NVIDIA NIM API key and accessible endpoint access.
- Open-source distribution under repository `arunCSK/arun-code`.
