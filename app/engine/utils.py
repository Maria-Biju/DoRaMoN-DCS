from __future__ import annotations
from typing import Dict, List


def renormalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    Convert any non-negative weights into a normalized distribution that sums to 1.
    If all are 0, assign equal weights.
    """
    s = sum(max(0.0, w) for w in weights.values())
    if s == 0:
        n = len(weights)
        return {k: 1.0 / n for k in weights}
    return {k: max(0.0, w) / s for k, w in weights.items()}


def normalize_minmax(values: List[float], goal: str) -> List[float]:
    """
    Min-max normalize values into [0, 1].
    goal:
      - "benefit": higher is better
      - "cost": lower is better (inverted)
    """
    mn = min(values)
    mx = max(values)

    # Edge case: all equal → no discrimination, treat all equal
    if mx == mn:
        return [1.0 for _ in values]

    if goal == "benefit":
        return [(v - mn) / (mx - mn) for v in values]

    # cost: lower is better → invert
    return [(mx - v) / (mx - mn) for v in values]
