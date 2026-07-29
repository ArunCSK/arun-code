# Speckit Development Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### Spec-First Development
<!-- Example: I. Library-First -->
All features start with a formal specification that defines scope, requirements, and acceptance criteria before any code is written.
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### Test-Driven Implementation
<!-- Example: II. CLI Interface -->
Automated tests are written alongside specifications; code must pass all tests before integration.
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### Modular Library Architecture
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
Each feature is implemented as a self‑contained library with a clear public API, enabling reuse and independent testing.
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### Continuous Integration & Automated Verification
<!-- Example: IV. Integration Testing -->
Every change triggers CI pipelines that run linting, tests, and verify constitution consistency.
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### Documentation and Versioning
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
Documentation is generated from spec and code; version numbers follow semantic versioning with explicit change logs.
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

## Constraints
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

Include performance targets, security requirements, and compatibility guidelines for the speckit tooling.
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## Development Workflow
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

Outline the workflow: spec authoring → review → test generation → implementation → CI verification → release.
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

All changes to the constitution must be reviewed via a pull request; amendments require approval from at least two core maintainers and must be reflected in the spec templates.
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: 0.2.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2026-07-29
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
