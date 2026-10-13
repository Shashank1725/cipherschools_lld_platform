# Research Note: Helping Learners Practise Low-Level Design

## Learner problem
LLD interviews ask candidates to translate requirements into collaborating classes and interfaces, define responsibilities, model object relationships, and explain trade-offs. A learner may produce a plausible design but remain unsure whether classes have focused responsibilities, relationships are clear, or edge cases have been considered. Feedback is most useful when it points to concrete evidence and a next action.

## Existing approaches considered
This note is a short product-oriented desk-research summary, not a claim of exhaustive market research.

- **Interview-preparation platforms and question banks** commonly help users discover prompts and practise recurring topics. A prompt catalogue is useful, but by itself it does not ensure that learners get actionable feedback on their own designs.
- **Collaborative diagramming tools** make it easy to draw classes and relationships. They provide a canvas, but diagram syntax alone does not explain whether a responsibility is cohesive or why one design trade-off is preferable.
- **General-purpose AI chat assistants** can critique a design conversationally. Their feedback can be broad or inconsistent unless the prompt provides a stable rubric, asks for evidence, and separates uncertainty from facts.
- **Repositories and articles containing worked solutions** can show one possible design. The risk is that learners compare their own solution to a single canonical answer even though multiple designs may be reasonable.

These are categories of approaches rather than a benchmark of specific vendors. The prototype deliberately avoids claiming that a particular product lacks a feature without a verified product-by-product audit.

## Product gap and direction
The MVP combines a small curated problem set with a structured submission and a repeatable review rubric. Instead of requiring UML tooling, the learner lists classes and responsibilities, describes relationships, and explains patterns, trade-offs, and edge cases. The evaluator then provides dimension-level feedback and suggested next steps.

## Principles
1. **Evidence over verdicts:** feedback should say what the submission demonstrates or what is missing.
2. **Plurality of valid designs:** patterns are optional; justification matters more than naming a pattern.
3. **Actionable iteration:** history should make it easy to revise and compare attempts.
4. **Trustworthy automation:** deterministic checks handle validation and simple signals; subjective critique can later use an LLM with explicit uncertainty.
5. **Focused scope:** three representative problems and one complete practice loop are more valuable than a large LMS or distributed architecture.
