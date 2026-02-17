from __future__ import annotations

from typing import Dict, List

from app.api.schemas import Scenario
from app.engine.utils import normalize_minmax, renormalize_weights


def evaluate_wsm(scenario: Scenario) -> List[str]:
    """
    MCDA - Weighted Sum Model (WSM)
    Returns a ranked list of option names (best first).

    Assumptions for Part 3 MVP:
    - Only numeric criteria are supported.
    - Options must contain a numeric value for every criterion.
    - Weights can be any non-negative numbers; internally normalized.
    """
    if len(scenario.criteria) == 0:
        raise ValueError("At least one criterion is required.")
    if len(scenario.options) < 2:
        raise ValueError("At least two options are required.")

    # weights normalized
    w_raw = {c.id: float(c.weight) for c in scenario.criteria}
    w = renormalize_weights(w_raw)

    # collect raw numeric values per criterion
    raw_by_criterion: Dict[str, List[float]] = {c.id: [] for c in scenario.criteria}

    for opt in scenario.options:
        for c in scenario.criteria:
            if c.id not in opt.values:
                raise ValueError(f"Option '{opt.name}' missing value for criterion '{c.name}' ({c.id}).")

            v = opt.values[c.id]
            if not isinstance(v, (int, float)):
                raise ValueError(
                    f"Criterion '{c.name}' expects a number in Part 3 (got {type(v).__name__})."
                )
            raw_by_criterion[c.id].append(float(v))

    # normalize each criterion into [0,1] based on goal
    norm_by_criterion: Dict[str, List[float]] = {}
    for c in scenario.criteria:
        norm_by_criterion[c.id] = normalize_minmax(raw_by_criterion[c.id], c.goal)

    # compute weighted sum score per option
    scores: List[float] = [0.0 for _ in scenario.options]
    for i, _opt in enumerate(scenario.options):
        total = 0.0
        for c in scenario.criteria:
            total += w[c.id] * float(norm_by_criterion[c.id][i])
        scores[i] = total

    # rank by score descending
    indexed = list(enumerate(scenario.options))
    indexed.sort(key=lambda pair: scores[pair[0]], reverse=True)

    return [opt.name for _, opt in indexed]
