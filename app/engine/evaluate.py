from __future__ import annotations

from typing import Dict, List

from app.api.schemas import Scenario, OptionExplanation
from app.engine.utils import normalize_minmax, renormalize_weights


def evaluate_wsm(scenario: Scenario) -> List[OptionExplanation]:
    """
    MCDA - Weighted Sum Model (WSM)

    Part 5 update:
    - Returns detailed results per option (score + per-criterion contributions)
      so the API/UI can explain *why* an option ranked #1.

    Current assumptions (still MVP-friendly):
    - Only numeric criteria are supported.
    - Options must contain a numeric value for every criterion.
    - Weights can be any non-negative numbers; internally normalized.
    """
    if len(scenario.criteria) == 0:
        raise ValueError("At least one criterion is required.")
    if len(scenario.options) < 2:
        raise ValueError("At least two options are required.")

    # Normalize weights
    w_raw = {c.id: float(c.weight) for c in scenario.criteria}
    w = renormalize_weights(w_raw)

    # Collect raw numeric values per criterion across options
    raw_by_criterion: Dict[str, List[float]] = {c.id: [] for c in scenario.criteria}

    for opt in scenario.options:
        for c in scenario.criteria:
            if c.id not in opt.values:
                raise ValueError(f"Option '{opt.name}' missing value for criterion '{c.name}' ({c.id}).")

            v = opt.values[c.id]
            if not isinstance(v, (int, float)):
                raise ValueError(
                    f"Criterion '{c.name}' expects a number in Part 5 (got {type(v).__name__})."
                )
            raw_by_criterion[c.id].append(float(v))

    # Normalize each criterion into [0,1] based on goal (benefit/cost)
    norm_by_criterion: Dict[str, List[float]] = {}
    for c in scenario.criteria:
        norm_by_criterion[c.id] = normalize_minmax(raw_by_criterion[c.id], c.goal)

    # Compute score + contributions per option
    results: List[OptionExplanation] = []

    for i, opt in enumerate(scenario.options):
        total_score = 0.0
        contributions: Dict[str, float] = {}

        for c in scenario.criteria:
            contrib = float(w[c.id]) * float(norm_by_criterion[c.id][i])
            contributions[c.id] = round(contrib, 4)
            total_score += contrib

        results.append(
            OptionExplanation(
                name=opt.name,
                score=round(total_score, 4),
                contributions=contributions
            )
        )

    # Rank by score descending
    results.sort(key=lambda r: r.score, reverse=True)
    return results