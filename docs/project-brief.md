# Project Brief

> **Fill this out immediately after running `@kodevibe/harness init`.** The pm agent uses this file for Direction Guard. Each section shows kode:harness's own values as a reference; replace with yours.

## Vision

_Example (kode:harness)_: Keep AI coding agents aligned on project direction across sessions and teammates, via markdown-native guardrails inside whichever IDE the developer uses.

<!-- What is this project and why does it exist? Keep it to 1-2 sentences. The north star for all decisions. Replace the example above with your own. -->

## Goals

_Example (kode:harness)_:
- Persist project memory across LLM sessions via 5 markdown state files.
- Detect direction drift before code is written (Direction Guard in pm/lead/reviewer).
- Stay lightweight: ≤30 files, ≤40K tokens. Zero runtime deps. MIT.
- Support 6 IDEs with one `npx` install.

<!-- 3-5 concrete, measurable goals. Replace the example above with your own. -->

## Non-Goals

_Example (kode:harness)_:
- Not a runtime / SDK — we ship instructions, not LLM execution.
- Not a project-management replacement — state files coordinate AI, not standups.
- Not solo-only — multi-developer alignment is the differentiator.
- Not a UI/dashboard — markdown in the repo is the interface.

<!-- Explicitly OUT OF SCOPE. The pm agent WARNs when a request falls here. Replace the example above with your own. -->

## Target Users

_Example (kode:harness)_: Developers and small teams (1–10) using AI coding assistants daily, who have felt their AI "forget" decisions and prefer markdown-in-repo over a SaaS dashboard.

<!-- Who is this for? Be specific. Replace the example above with your own. -->

## Done Definition

<!-- What makes the project or first usable slice releasable? Keep this to 3-5 observable checks.
   Example:
   - [ ] User can complete the core workflow end-to-end
   - [ ] Automated tests pass
   - [ ] Smoke proof confirms the app/CLI responds
-->

## Success Proof

<!-- How will the user know this works? Prefer commands, metrics, or manual checks.
   Example:
   - Test command: npm test
   - Smoke proof: npm run build && npm start
   - Manual proof: create item → refresh → item persists
-->

## Project Docs Hub Index

<!-- Optional — maintained by the `docs-bridge` skill when the project needs to
   connect local documentation to a wiki/docs hub without copying whole documents.
   Keep originals in place; index repo-relative paths, roles, sync intent,
   sanitized hub aliases, and visibility boundaries here. Machine-specific
   resolver details belong in ignored `.harness/docs-bridge.local.*` files.

   | Local Source | Role | Hub Target | Sync Direction | Visibility | Status | Last Reviewed |
   |--------------|------|------------|----------------|------------|--------|---------------|
   | README.md | source | local-only | local-source -> hub-summary | public | active | YYYY-MM-DD |

   Role: source, planning-artifact, decision-record, reference, runbook, state, generated
   Sync Direction: local-source -> hub-summary, hub-reference -> local-index, bidirectional-index-only, local-only
   Visibility: public, team, company-confidential, personal-private, do-not-share
   Status: active, proposed, stale, archived
-->


## Key Technical Decisions

<!-- Record foundational technology choices AND workflow conventions.
   Helps LLMs generate correct code and follow your team's workflow.

   **Technology Stack** (fill all that apply):
   - Language: <!-- e.g., TypeScript 5.x (strict mode), Python 3.12, Go 1.22 -->
   - Framework: <!-- e.g., Express + Prisma ORM, Django 5.0, Spring Boot 3.x -->
   - Test runner: <!-- e.g., Vitest (not Jest), pytest, JUnit 5 -->
   - Database: <!-- e.g., PostgreSQL 16, MongoDB 7, SQLite -->
   - Architecture: <!-- e.g., Hexagonal (Port + Adapter), Layered, Clean Architecture -->

   **Workflow Conventions** (fill all that apply):
   - Default branch: <!-- e.g., main, develop -->
   - Git remote: <!-- e.g., origin, upstream -->
   - Staging policy: <!-- e.g., explicit per-file staging (no git add .), allow git add . -->
   - Branch strategy: <!-- e.g., feature branches (feature/S1-1-scaffolding), trunk-based, gitflow -->
   - Commit message format: <!-- default: "S{N}-{M}: {description}" — Story ID prefix for traceability -->
   - Push frequency: <!-- e.g., per Story completion, per session end, per sprint -->
   - Pivot authority: <!-- e.g., team consensus, tech lead, solo developer -->
   - Deploy method: <!-- e.g., npm publish, docker push, terraform apply -->
-->

## Decision Log

<!-- Record WHY key decisions were made. The pm agent uses this to avoid re-debating settled decisions.
   Use the `pivot` skill to add entries here when direction changes.
   Format:

### [YYYY-MM-DD] [Decision Title]
- **Change**: What changed
- **Reason**: Why this decision was made
- **Impact**: What was affected
- **Alternatives Considered**: 1-2 bullet points on what was rejected and why
-->
