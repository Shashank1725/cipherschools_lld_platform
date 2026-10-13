"""Explainable heuristic evaluator for the LLD Practice Platform MVP.

This is a rubric-based heuristic, not a compiler or proof of design correctness.
"""
from __future__ import annotations
import re
from typing import Protocol
from .schemas import AttemptCreate


class Evaluator(Protocol):
    def evaluate(self, submission: AttemptCreate) -> dict: ...


class RubricEvaluator:
    # Internal rubric weights total 100. Optional patterns are not required to pass.
    WEIGHTS = {
        "Class responsibilities": 20,
        "Relationships and collaboration": 25,
        "Trade-off reasoning": 20,
        "Pattern justification": 10,
        "Edge cases and recovery": 25,
    }

    @staticmethod
    def _words(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z][a-zA-Z0-9_-]*", text.lower()))

    @staticmethod
    def _has(text: str, terms: tuple[str, ...]) -> bool:
        lowered = text.lower()
        return any(term in lowered for term in terms)

    def evaluate(self, submission: AttemptCreate) -> dict:
        class_names = [item.name.strip().lower() for item in submission.classes]
        responsibilities = [item.responsibility.strip() for item in submission.classes]
        all_responsibilities = " ".join(responsibilities).lower()
        relationships = submission.relationships_text.strip().lower()
        patterns = submission.patterns.strip().lower()
        tradeoffs = submission.tradeoffs.strip().lower()
        edge_cases = submission.edge_cases.strip().lower()
        combined = " ".join([all_responsibilities, relationships, patterns, tradeoffs, edge_cases])

        # 0-4 rubric levels: missing/vague, partial, specific, detailed and justified.
        duplicate_names = len(class_names) != len(set(class_names))
        broad_phrases = ("handles everything", "does everything", "all logic", "one class does all")
        focused_signals = sum(self._has(r.lower(), (
            "responsible for", "only", "validates", "calculates", "stores", "manages",
            "coordinates", "persists", "reserves", "dispenses", "processes"
        )) for r in responsibilities)
        distinct_responsibilities = len(set(responsibilities)) >= max(2, len(responsibilities) // 2)
        if duplicate_names or self._has(all_responsibilities, broad_phrases):
            class_level = 0
            class_feedback = "Avoid duplicate or catch-all classes; give each class one clear responsibility."
        else:
            ratio = focused_signals / max(1, len(responsibilities))
            class_level = 1 + int(ratio >= 0.5) + int(ratio >= 0.8 and distinct_responsibilities)
            if len(responsibilities) >= 3 and distinct_responsibilities:
                class_level = min(4, class_level + 1)
            class_level = min(4, class_level)
            class_feedback = "Define a single responsibility per class and make responsibilities distinct and testable."

        # Relationship quality requires collaboration/workflow signals, not merely word count.
        interaction = self._has(relationships, (
            "calls", "uses", "delegates", "sends", "returns", "notifies", "owns", "contains",
            "depends on", "communicates", "passes", "invokes", "collaborates", "one-to-many", "many-to-one"
        ))
        concrete_flow = self._has(relationships, (
            "first", "then", "after", "before", "once", "if payment", "payment succeeds",
            "reserve", "reservation", "confirm", "release", "refund", "dispense", "sequence"
        ))
        named_classes = sum(1 for name in class_names if len(name) > 1 and name in relationships)
        ownership_or_cardinality = self._has(relationships, (
            "owns", "contains", "one-to-many", "many-to-one", "one-to-one", "has many", "composition", "aggregation"
        ))
        relationship_level = min(4, int(interaction) + int(named_classes >= 2) + int(concrete_flow) + int(ownership_or_cardinality))
        relationship_feedback = "Name the collaborating classes and describe call direction, ownership/cardinality, and the order of interactions."

        alternative = self._has(tradeoffs, ("alternative", "instead", "versus", "vs", "compared with", "another approach", "could use"))
        benefit = self._has(tradeoffs, ("because", "benefit", "advantage", "simpler", "faster", "easier", "improves", "reduces"))
        cost = self._has(tradeoffs, ("cost", "trade-off", "tradeoff", "however", "but", "downside", "drawback", "complexity", "maintenance", "slower"))
        concrete_choice = self._has(tradeoffs, ("interface", "strategy", "inheritance", "composition", "single class", "separate class", "database", "in-memory", "synchronous", "asynchronous"))
        tradeoff_level = min(4, int(alternative) + int(benefit) + int(cost) + int(concrete_choice))
        tradeoff_feedback = "Compare at least one realistic alternative and explain both the benefit and the cost of your choice."

        no_pattern_rationale = self._has(patterns, ("no pattern", "none needed", "not needed", "unnecessary", "simple enough", "avoid overengineering"))
        pattern_name = self._has(patterns, ("strategy", "factory", "observer", "state pattern", "singleton", "repository", "adapter", "command", "dependency injection"))
        pattern_why = self._has(patterns, ("because", "so that", "allows", "helps", "when", "useful", "reason", "benefit"))
        pattern_tradeoff = self._has(patterns, ("trade-off", "tradeoff", "overhead", "complexity", "drawback", "instead of", "avoid"))
        if not patterns:
            pattern_level = 0
            pattern_feedback = "Patterns are optional: briefly justify why none is needed, or name a pattern and explain its fit."
        elif no_pattern_rationale:
            pattern_level = 3 if pattern_why or self._has(patterns, ("because", "since", "given")) else 2
            if pattern_tradeoff:
                pattern_level = 4
            pattern_feedback = "Your no-pattern decision should be tied to the problem's simplicity and the cost of extra abstraction."
        elif pattern_name:
            pattern_level = 1 + int(pattern_why) + int(pattern_tradeoff)
            pattern_level = min(4, pattern_level)
            pattern_feedback = "Explain which changing behaviour the pattern isolates and what complexity it introduces."
        else:
            pattern_level = 1
            pattern_feedback = "Naming no pattern or listing a buzzword is not enough; explain why the choice fits."

        failure = self._has(edge_cases, ("fail", "failure", "exception", "unavailable", "timeout", "crash", "error", "disconnect"))
        boundary = self._has(edge_cases, ("empty", "full", "invalid", "negative", "zero", "limit", "out of stock", "insufficient", "duplicate", "concurrent"))
        recovery = self._has(edge_cases, ("refund", "retry", "rollback", "release", "restore", "cancel", "recover", "fallback", "mark failed", "compensat"))
        expected_outcome = self._has(edge_cases, ("should", "must", "then", "instead", "return", "reject", "do not", "never", "remain", "state"))
        edge_level = min(4, int(failure) + int(boundary) + int(recovery) + int(expected_outcome))
        edge_feedback = "For each important failure, state the trigger, expected state change, and recovery action (for example refund or release reservation)."

        # Contradictions that are especially dangerous for a vending-machine design.
        contradiction_notes = []
        if self._has(combined, ("payment fails", "payment failed", "payment failure")) and self._has(combined, ("dispense anyway", "still dispense", "dispense regardless")):
            contradiction_notes.append("Design contradiction: the product must not be dispensed when payment has failed.")
        if self._has(combined, ("dispensing fails", "dispense fails", "dispense failure")) and self._has(combined, ("keep payment", "no refund", "never refund")):
            contradiction_notes.append("Design contradiction: define a refund or recoverable pending state when dispensing fails after payment.")
        if self._has(combined, ("concurrent", "simultaneous", "race condition")) and self._has(combined, ("same item", "last item", "double-book", "oversell")) and not self._has(combined, ("atomic", "lock", "transaction", "reservation")):
            contradiction_notes.append("Concurrency gap: explain atomic stock reservation, locking, or a database transaction.")

        levels = {
            "Class responsibilities": class_level,
            "Relationships and collaboration": relationship_level,
            "Trade-off reasoning": tradeoff_level,
            "Pattern justification": pattern_level,
            "Edge cases and recovery": edge_level,
        }
        feedback_by_name = {
            "Class responsibilities": class_feedback,
            "Relationships and collaboration": relationship_feedback,
            "Trade-off reasoning": tradeoff_feedback,
            "Pattern justification": pattern_feedback,
            "Edge cases and recovery": edge_feedback,
        }
        dimensions = []
        score = 0
        for name, weight in self.WEIGHTS.items():
            level = levels[name]
            earned = round(weight * level / 4)
            score += earned
            dimensions.append({
                "dimension": name,
                "passed": level >= 3,
                "level": level,
                "max_level": 4,
                "weight": weight,
                "score": earned,
                "max_score": weight,
                "principle": feedback_by_name[name],
                "feedback": ("Strong signal: " if level >= 3 else "Needs work: ") + feedback_by_name[name],
            })

        if contradiction_notes:
            score = max(0, score - min(20, 8 * len(contradiction_notes)))
        score = min(100, max(0, score))
        strengths = [f"{d['dimension']} ({d['score']}/{d['max_score']})" for d in dimensions if d["level"] >= 3]
        improvements = [d["feedback"] for d in dimensions if d["level"] < 3]
        improvements.extend(contradiction_notes)
        return {
            "summary": "Heuristic rubric feedback: use it to guide revision, not as proof that a design is correct.",
            "score": score,
            "dimensions": dimensions,
            "strengths": strengths or ["You have a starting point; make the design decisions more specific."],
            "improvements": improvements or ["Review concurrency, state transitions, and failure recovery for hidden gaps."],
            "next_step": "Improve the lowest-scoring dimension with one concrete class interaction, alternative, or failure-recovery sequence.",
        }
