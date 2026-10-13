# AI Usage & Engineering Judgement Notes

This document reflects how AI assistance was integrated as a collaborative design and coding partner throughout this 2-day engineering assignment, detailing where AI recommendations were accepted, rejected, or modified using human engineering judgement.

---

### Decision 1: Structured Multi-Field Submission vs. Free-Text / UML Canvas
- **AI Suggestion**: Build either a drag-and-drop UML diagram editor or accept a single Markdown / free-text essay.
- **Accepted / Rejected**: **Modified & Selected Structured Schema**.
- **Human Engineering Judgement**:
  - A diagram canvas within a 2-day scope would consume 80% of development effort on canvas UI rendering rather than domain evaluation.
  - Conversely, an unstructured free-text input makes automated parsing ambiguous and leaves learners guessing what to write.
  - **Decision**: Implemented structured dimensions (`classes with single responsibilities`, `relationships & collaboration`, `pattern justification`, `trade-offs`, and `edge cases`). This guides the learner through genuine LLD thought processes while keeping validation deterministic and explainable.

---

### Decision 2: Deterministic Rubric Evaluator vs. Raw LLM Grading
- **AI Suggestion**: Send the learner's design directly to an OpenAI/Gemini prompt with a prompt like *"Grade this LLD design from 0 to 100"*.
- **Accepted / Rejected**: **Rejected raw LLM grading; Accepted Deterministic Rubric with an Extensible Protocol**.
- **Human Engineering Judgement**:
  - Direct LLM scoring is prone to prompt nondeterminism, grade inflation, latency spikes, and requires third-party API keys that can fail or rate-limit during evaluation.
  - Furthermore, in LLD there is rarely a single "correct" canonical answer; penalizing a valid alternative design damages learner trust.
  - **Decision**: Built a local, explainable, multi-dimensional rubric (`RubricEvaluator`). It produces reliable feedback scores, detects design contradictions (e.g., dispensing goods upon failed payments), and highlights missing considerations.

---

### Decision 3: Decoupled Evaluator Contract via Python `Protocol`
- **AI Suggestion**: Place scoring functions directly inside FastAPI route handlers for simplicity.
- **Accepted / Rejected**: **Rejected route coupling; Accepted Protocol-based Evaluator Interface**.
- **Human Engineering Judgement**:
  - Hardcoding grading heuristics into API endpoints violates the Open/Closed Principle and prevents adding new evaluation strategies.
  - **Decision**: Defined `Evaluator(Protocol)` with `evaluate(submission: AttemptCreate) -> dict`. In the future, an `LLMEvaluator`, a hybrid evaluator, or custom rubrics can be swapped in via dependency injection without modifying routes, schemas, or database models.

---

### Decision 4: Two-Phase Submission Persistence (Save-Before-Evaluation)
- **AI Suggestion**: Evaluate the submission in memory first, and only write to the database if evaluation finishes successfully.
- **Accepted / Rejected**: **Rejected; Inverted to Persist-First Architecture**.
- **Human Engineering Judgement**:
  - If evaluation fails (e.g. timeout, evaluation crash, external LLM failure), discarding the learner's attempt causes extreme frustration and data loss.
  - **Decision**: The attempt is immediately persisted with status `evaluating`. If the evaluation completes, status updates to `evaluated`. If it fails, status updates to `evaluation_failed` with a clean error message, and a dedicated retry endpoint (`POST /api/attempts/{id}/retry-evaluation`) allows the learner to re-evaluate without retyping.

---

### Decision 5: Practical Modular Monolith vs. Distributed Queue Worker
- **AI Suggestion**: Introduce Celery/Redis or RabbitMQ with separate worker microservices to handle background evaluation tasks.
- **Accepted / Rejected**: **Rejected for MVP scope**.
- **Human Engineering Judgement**:
  - As highlighted in the assignment's Scope Boundaries: *"This is primarily an LLD/domain-design exercise. Do not turn the assignment into a distributed-systems project."*
  - A synchronous evaluation pipeline takes less than 50ms locally. Adding Docker Compose, message brokers, and distributed state would introduce unnecessary operational overhead.
  - A background task worker can be cleanly introduced later behind the existing `Evaluator` interface if real LLM latency warrants it.

---

### Summary of Human Review
All generated code, schemas, and tests were locally verified, executed, and validated with `pytest` and `vite build` prior to commit.
