from __future__ import annotations

from typing import List, Tuple

from app.api.schemas import Constraint, Criterion, Option, FilteredOutOption


def _compare(v: float, op: str, target: float) -> bool:
    if op == "<=":
        return v <= target
    if op == "<":
        return v < target
    if op == ">=":
        return v >= target
    if op == ">":
        return v > target
    if op == "==":
        return v == target
    raise ValueError(f"Unsupported constraint operator: {op}")


def apply_constraints(
    criteria: List[Criterion],
    options: List[Option],
    constraints: List[Constraint],
) -> Tuple[List[Option], List[FilteredOutOption]]:
    """
    Returns: (kept_options, filtered_out_with_reasons)
    """
    if not constraints:
        return options, []

    crit_name = {c.id: c.name for c in criteria}

    kept: List[Option] = []
    filtered: List[FilteredOutOption] = []

    for opt in options:
        reasons: List[str] = []
        for con in constraints:
            if con.criterion_id not in opt.values:
                reasons.append(
                    f"Missing value for '{crit_name.get(con.criterion_id, con.criterion_id)}' ({con.criterion_id})"
                )
                continue

            raw = opt.values[con.criterion_id]
            if not isinstance(raw, (int, float)):
                reasons.append(
                    f"Non-numeric value for '{crit_name.get(con.criterion_id, con.criterion_id)}' ({con.criterion_id})"
                )
                continue

            v = float(raw)
            ok = _compare(v, con.op, float(con.value))
            if not ok:
                cname = crit_name.get(con.criterion_id, con.criterion_id)
                reasons.append(f"{cname} must be {con.op} {con.value} (got {v})")

        if reasons:
            filtered.append(FilteredOutOption(name=opt.name, reasons=reasons))
        else:
            kept.append(opt)

    return kept, filtered