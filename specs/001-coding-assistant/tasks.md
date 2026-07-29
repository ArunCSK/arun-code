# Tasks: Arun-Code Local Coding Assistant

**Input**: Design documents from `/specs/001-coding-assistant/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, uv package setup, and basic directory structure

- [x] T001 Create pyproject.toml with uv build configuration at pyproject.toml
- [x] T002 Create arun_code package directory with arun_code/__init__.py
- [x] T003 [P] Create .gitignore with Python patterns at .gitignore
- [x] T004 [P] Create .env.example with required environment variables at .env.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration and NIM client that all user stories depend on

- [x] T005 Implement configuration loader in arun_code/config.py
- [x] T006 Implement NVIDIA NIM HTTP client wrapper in arun_code/nim_client.py
- [x] T007 Create shared data models (ChatMessage, AgentResponse) in arun_code/models.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Local Agent Mode Prompting & Execution (Priority: P1) -- MVP

**Goal**: Send prompts via CLI or server, execute agent tool calls, return human-friendly NIM responses

**Independent Test**: Run `uv run python -m arun_code.main "Hello"` and verify a response is printed

### Implementation for User Story 1

- [x] T008 [US1] Implement CLI entry point in arun_code/main.py
- [x] T009 [US1] Implement agent tool execution engine in arun_code/agent.py
- [x] T010 [US1] Implement FastAPI server with /v1/chat/completions endpoint in arun_code/server.py
- [x] T011 [US1] Add error handling for NIM 404 and auth failures in arun_code/nim_client.py

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - VS Code & Antigravity IDE Integration (Priority: P2)

**Goal**: IDE extensions connect to local server for chat interactions

**Independent Test**: Start server and send POST to localhost:8000/v1/chat/completions from IDE extension

### Implementation for User Story 2

- [x] T012 [US2] Add /health endpoint and CORS middleware to arun_code/server.py
- [x] T013 [US2] Create VS Code extension scaffold in vscode-extension/

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Graceful Error Handling & Diagnostics (Priority: P3)

**Goal**: Clear user-facing error messages for NIM API failures including 404 function errors

**Independent Test**: Supply invalid endpoint and verify friendly error output

### Implementation for User Story 3

- [x] T014 [US3] Add structured error response formatting in arun_code/errors.py
- [x] T015 [US3] Wire error formatting into server and CLI error paths in arun_code/server.py and arun_code/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, tests, CI, final cleanup

- [x] T016 [P] Write unit tests for config and nim_client in tests/unit/test_config.py and tests/unit/test_nim_client.py
- [x] T017 [P] Write integration test for server in tests/integration/test_server.py
- [x] T018 [P] Create README.md with installation, configuration, and usage instructions at README.md
- [x] T019 Create GitHub Actions CI workflow at .github/workflows/ci.yml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Can start after US1 server endpoint exists (Phase 3)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2)

### Parallel Opportunities

- T003 and T004 can run in parallel (Setup phase)
- T016 and T017 can run in parallel (Polish phase)
- T018 can run in parallel with T016/T017

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Run CLI and server to verify end-to-end flow
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational --> Foundation ready
2. User Story 1 --> Test independently (MVP)
3. User Story 2 --> Test IDE integration
4. User Story 3 --> Test error handling
5. Polish --> CI, docs, tests
