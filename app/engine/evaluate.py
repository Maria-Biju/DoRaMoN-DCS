from __future__ import annotations

from typing import Dict, List, Tuple

from app.api.schemas import Scenario, OptionExplanation, FilteredOutOption, Option
from app.engine.constraints import apply_constraints
from app.engine.utils import normalize_minmax, renormalize_weights


def _top_k_contributors(pairs: List[Tuple[str, float]], k: int = 2) -> List[str]:
    """Return top-k criterion names by contribution (descending)."""
    pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)
    return [name for name, _ in pairs_sorted[:k]]


def _bottom_k_contributors(pairs: List[Tuple[str, float]], k: int = 2) -> List[str]:
    """Return bottom-k criterion names by contribution (ascending)."""
    pairs_sorted = sorted(pairs, key=lambda x: x[1])
    return [name for name, _ in pairs_sorted[:k]]


def evaluate_wsm(scenario: Scenario) -> Tuple[List[OptionExplanation], List[FilteredOutOption]]:
    """
    MCDA - Weighted Sum Model (WSM)

    Part 8 update:
    - Applies hard constraints BEFORE scoring.
    - Returns:
        (ranked option explanations, filtered_out options with reasons)

    Still deterministic & explainable:
    - weights normalized
    - values normalized to [0,1] with cost/benefit handling
    - contributions, strengths/weaknesses, and short why message
    """
    if len(scenario.criteria) == 0:
        raise ValueError("At least one criterion is required.")
    if len(scenario.options) < 2:
        raise ValueError("At least two options are required.")

    # ---------- Part 8: apply constraints first ----------
    kept_options, filtered_out = apply_constraints(
        criteria=scenario.criteria,
        options=scenario.options,
        constraints=getattr(scenario, "constraints", []) or []
    )

    # If constraints remove too many options, ranking doesn't make sense
    if len(kept_options) < 2:
        return [], filtered_out

    # Map criterion id -> name (for human readable output)
    criterion_name: Dict[str, str] = {c.id: c.name for c in scenario.criteria}

    # Normalize weights
    w_raw = {c.id: float(c.weight) for c in scenario.criteria}
    w = renormalize_weights(w_raw)

    # Collect raw numeric values per criterion across kept options
    raw_by_criterion: Dict[str, List[float]] = {c.id: [] for c in scenario.criteria}

    for opt in kept_options:
        for c in scenario.criteria:
            if c.id not in opt.values:
                raise ValueError(f"Option '{opt.name}' missing value for criterion '{c.name}' ({c.id}).")

            v = opt.values[c.id]
            if not isinstance(v, (int, float)):
                raise ValueError(
                    f"Criterion '{c.name}' expects a number (got {type(v).__name__})."
                )
            raw_by_criterion[c.id].append(float(v))

    # Normalize each criterion into [0,1] based on goal (benefit/cost)
    norm_by_criterion: Dict[str, List[float]] = {}
    for c in scenario.criteria:
        norm_by_criterion[c.id] = normalize_minmax(raw_by_criterion[c.id], c.goal)

    # Compute score + contributions + explanation fields per option
    results: List[OptionExplanation] = []

    for i, opt in enumerate(kept_options):
        total_score = 0.0
        contributions: Dict[str, float] = {}
        readable_pairs: List[Tuple[str, float]] = []  # (criterion_name, contribution)

        for c in scenario.criteria:
            contrib = float(w[c.id]) * float(norm_by_criterion[c.id][i])
            contrib_r = round(contrib, 4)
            contributions[c.id] = contrib_r
            total_score += contrib
            readable_pairs.append((criterion_name[c.id], contrib_r))

        total_score_r = round(total_score, 4)

        # strengths & weaknesses: pick top/bottom 2 by contribution
        strengths = _top_k_contributors(readable_pairs, k=min(2, len(readable_pairs)))
        weaknesses = _bottom_k_contributors(readable_pairs, k=min(2, len(readable_pairs)))

        # Template-based short explanation
        strength_text = strengths[0] if len(strengths) == 1 else f"{strengths[0]} and {strengths[1]}"
        weakness_text = weaknesses[0] if len(weaknesses) == 1 else f"{weaknesses[0]} and {weaknesses[1]}"

        why = (
            f"Scored {total_score_r} mainly due to strong performance on {strength_text}. "
            f"Lower contribution came from {weakness_text}."
        )

        results.append(
            OptionExplanation(
                name=opt.name,
                score=total_score_r,
                contributions=contributions,   # criterion_id -> value
                strengths=strengths,
                weaknesses=weaknesses,
                why=why
            )
        )

    # Rank by score descending
    results.sort(key=lambda r: r.score, reverse=True)

    return results, filtered_out