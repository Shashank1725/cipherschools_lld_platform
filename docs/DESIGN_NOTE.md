# Design Note

## MVP and learner flow
Problem catalogue → problem requirements → structured attempt → saved submission → rubric feedback → history → revised attempt.

Each problem includes a summary, requirements, constraints, difficulty, and time estimate. An attempt records the learner's class list, relationships, patterns, trade-offs, edge cases, status, score, and feedback.

## Domain model
- `Problem`: stable problem definition and requirements.
- `Attempt`: one immutable-in-intent submission and its evaluation result. A later revision creates a new attempt, preserving history.
- `Evaluator`: contract for turning a validated submission into structured feedback.
- `RubricEvaluator`: default deterministic implementation.
- `AttemptCreate` / `AttemptOut`: API boundary schemas that validate input and shape output.

## Evaluation
The current rubric examines responsibility clarity, relationship modelling, trade-off awareness, pattern justification, and edge-case thinking. The score is the percentage of rubric dimensions passed. It is a coaching signal, not a judgement of absolute correctness. A design can pass while still having issues and can fail a heuristic despite being defensible; human review remains important.

Deterministic validation is used for field lengths, class count, known problem IDs, and attempt existence. Text heuristics are used only for simple feedback signals. A future LLM evaluator should receive problem context plus a rubric, return evidence-linked observations and confidence, and avoid inventing requirements. It should be added behind `Evaluator`, not coupled to routes.

## Failure handling
The API persists an attempt before evaluation. If evaluation raises an exception, the attempt is retained with `evaluation_failed` status and a retry endpoint is provided. The current evaluator is synchronous and fast. If an LLM makes evaluation slow, a background task/worker and polling can be added without changing the domain contract.

## Key trade-offs
- **Structured text instead of diagram editor:** easier to implement and validate in two days; a diagram submission adapter can be added later.
- **SQLite default:** zero setup for reviewers; SQLAlchemy allows PostgreSQL via configuration.
- **Heuristic feedback:** repeatable and no secrets needed, but shallow; it is explicitly presented as a checklist.
- **No authentication:** learner ID is a demo field only; real deployment needs secure identity and authorization.
- **Simple monolith:** suitable for assignment scale and avoids unnecessary infrastructure.
