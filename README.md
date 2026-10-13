# Craft — LLD Practice Platform

A focused, end-to-end MVP for the CipherSchools 2-day engineering assignment. Learners choose a Low-Level Design (LLD) problem, submit a structured solution, receive transparent, explainable feedback, and iterate on earlier attempts.

---

## 📌 Executive Summary & Assignment Alignment

This prototype demonstrates the complete core learner loop:
```
Choose Problem ➔ Formulate Design ➔ Submit ➔ Receive Explainable Rubric Feedback ➔ Review History ➔ Iterate
```

- **Domain-First Focus**: Concentrates on core LLD concepts (classes, responsibilities, relationships, trade-offs, and failure recoveries) rather than overengineering LMS administrative systems or distributed architectures.
- **Explainable Evaluation**: Uses a deterministic 5-dimension rubric evaluator that treats design evaluation as coaching signals rather than single-canonical-answer dogma.
- **Extensible Architecture**: Employs an `Evaluator` interface/protocol, allowing drop-in replacement with an LLM evaluator or multi-agent reviewer in the future.
- **Fail-Safe Iteration**: Submissions are persisted *before* evaluation runs to prevent learner data loss, with full attempt history and retry mechanisms.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic v2
- **Database**: SQLite (zero-config local default), PostgreSQL supported via `DATABASE_URL`
- **Frontend**: React 18, Vite, Lucide React (Vanilla CSS design system)
- **Testing**: pytest, FastAPI TestClient (HTTP integration, validation, and domain tests)

---

## 🚀 Quickstart & Running Locally

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend API server
python -m uvicorn app.main:app --reload
```
- **API Base URL**: `http://127.0.0.1:8000`
- **Swagger / OpenAPI Documentation**: `http://127.0.0.1:8000/docs`
- *Note*: SQLite database (`lld_practice.db`) is automatically initialized and seeded on first startup.

### 2. Frontend Setup

In a separate terminal:
```bash
cd frontend

# Install npm dependencies
npm install

# Start local development server
npm run dev
```
- Open the application in your browser at `http://localhost:5173`.
- *(Optional)* API URL override: create `frontend/.env` with `VITE_API_URL=http://127.0.0.1:8000`.

### 3. Run Automated Tests

```bash
cd backend
python -m pytest -q
```
Runs integration and unit test suites covering healthy API flow, invalid schemas (422), missing resources (404), evaluation scoring, learner history isolation, and conflict resolution (409).

---

## 🧭 Core Learner Journey

1. **Problem Selection**: Choose between curated problems (**Parking Lot**, **Elevator Controller**, **Vending Machine**), each with requirements, constraints, time estimates, and difficulty tiers.
2. **Structured Design Canvas**:
   - Class breakdown with dedicated Single Responsibility statements.
   - Collaborations, ownership, cardinality, and interaction flows.
   - Pattern justification (or explicit rationale for avoiding patterns to keep things simple).
   - Architectural trade-offs (benefits vs. drawbacks of chosen approaches).
   - Edge cases, race conditions, boundary conditions, and failure-recovery mechanisms.
3. **Multi-Dimensional Feedback**:
   - Overall score (0–100) reflecting rubric coverage.
   - Dimension-by-dimension breakdown:
     - *Class responsibilities* (20%)
     - *Relationships & collaboration* (25%)
     - *Trade-off reasoning* (20%)
     - *Pattern justification* (10%)
     - *Edge cases & recovery* (25%)
   - Explicit highlighting of design contradictions (e.g. dispensing items on failed payments).
   - Actionable "What is working", "Next improvements", and immediate "Your next step" guidance.
4. **Attempt History & Review**:
   - Every attempt is preserved with timestamps and scores.
   - Learners can load prior attempts back into the canvas to revise and see their score progress.

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check endpoint |
| `GET` | `/api/problems` | List all available practice problems |
| `GET` | `/api/problems/{problem_id}` | Get specific problem details, requirements, constraints |
| `POST` | `/api/attempts` | Submit an LLD solution for evaluation |
| `GET` | `/api/attempts/{attempt_id}` | Retrieve a specific attempt and its evaluation result |
| `GET` | `/api/problems/{problem_id}/attempts` | Query learner-specific attempt history |
| `POST` | `/api/attempts/{attempt_id}/retry-evaluation` | Retry evaluation on a previously failed submission |

---

## 🏛️ Key Engineering Decisions & Scope Boundaries

1. **Modular Monolith over Distributed Microservices**:
   For this 2-day assignment, building an asynchronous queue worker or multi-service architecture introduces accidental complexity. A clean modular FastAPI app with SQLAlchemy gives complete clarity and reliability.
2. **Deterministic Heuristics Before LLM**:
   LLMs can hallucinate or grade inconsistently. The initial MVP uses a transparent, deterministic rubric that acts as a consistent coaching checklist.
3. **Evaluator Behind a Strict Protocol**:
   The domain depends on `Evaluator(Protocol)` (`evaluate(submission) -> dict`). Pluggable evaluator backends (e.g. OpenAI/Anthropic/Gemini evaluators) can be introduced without changing route handlers or database schemas.
4. **Submission Persistence Before Evaluation**:
   If an evaluation engine crashes, times out, or errors, the user's work is never lost. The submission is persisted as `evaluating` / `evaluation_failed` and can be retried cleanly.
5. **Lightweight Auth for MVP**:
   The platform defaults to a demo learner context (`demo-learner`). In production, JWT/OAuth2 authentication and role-based permissions would be layered on.

---

## 📁 Repository Structure

```
cipherschools_lld_platform/
├── docs/
│   ├── RESEARCH_NOTE.md       # Learner problem research, tool gaps, & direction
│   └── DESIGN_NOTE.md         # Domain modeling, evaluator contracts, trade-offs
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entrypoint & REST routing
│   │   ├── models.py          # SQLAlchemy domain models (Problem, Attempt)
│   │   ├── schemas.py         # Pydantic validation schemas
│   │   ├── evaluation.py      # RubricEvaluator & Evaluator protocol
│   │   ├── database.py        # Database engine & session management
│   │   └── seed.py            # Seed data for curated LLD problems
│   ├── tests/                 # pytest test suite
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Single-page practice workspace, tabs, feedback
│   │   ├── styles.css         # Custom modern design system
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .gitignore                 # Clean repository exclusions (venv, db, node_modules)
├── README.md                  # Project overview & running instructions
└── AI_USAGE.md                # 5 meaningful AI-assisted decisions & judgements
```
