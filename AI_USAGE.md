# AI Usage Notes

This project used AI assistance as a coding and review partner. These are the meaningful decisions and the human judgement behind them.

1. **Structured submission instead of a single free-text answer**
   - AI suggestion: ask learners for classes, responsibilities, relationships, patterns, trade-offs, and edge cases.
   - Decision: accepted. These fields make the submission reviewable and create specific feedback without forcing a particular UML format.

2. **Deterministic rubric before LLM evaluation**
   - AI suggestion: combine basic deterministic checks with optional LLM reasoning.
   - Decision: accepted for the MVP. The rubric is explainable, repeatable, and works without API keys. It is deliberately labelled heuristic and does not claim there is only one correct design.

3. **Keep evaluation behind an interface**
   - AI suggestion: use an evaluator protocol to make future evaluation approaches replaceable.
   - Decision: accepted. The API depends on an evaluator contract rather than embedding rubric rules in route handlers.

4. **Save submission before evaluating**
   - AI suggestion: preserve a learner's work if feedback generation fails.
   - Decision: accepted. The attempt is persisted first, and a failed evaluation has a visible status plus retry endpoint.

5. **Avoid distributed-system overengineering**
   - AI suggestion: use queues and multiple services for slow evaluation.
   - Decision: rejected for this two-day prototype. A simple monolith is appropriate; a background worker can be introduced if real evaluation latency later justifies it.

AI-generated code and documentation should be reviewed, run, and tested before submission. Update this file if you make different implementation choices.
