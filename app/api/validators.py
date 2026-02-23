from __future__ import annotations

from typing import Set

from fastapi import HTTPException

from app.api.schemas import Scenario


def validate_scenario(s: Scenario) -> None:
    # Basic structure checks
    if not s.criteria:
        raise HTTPException(status_code=400, detail="At least one criterion is required.")
    if not s.options or len(s.options) < 2:
        raise HTTPException(status_code=400, detail="At least two options are required.")

    # Duplicate criterion IDs check
    seen: Set[str] = set()
    for c in s.criteria:
        if c.id in seen:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate criterion id '{c.id}'. Criterion ids must be unique."
            )
        seen.add(c.id)

    # Negative weight check (we allow 0, but not negative)
    for c in s.criteria:
        if c.weight < 0:
            raise HTTPException(
                status_code=400,
                detail=f"Criterion '{c.name}' ({c.id}) has negative weight. Weight must be >= 0."
            )

    # Missing values check (each option must provide every criterion id)
    required_ids = {c.id for c in s.criteria}
    for opt in s.options:
        missing = required_ids - set(opt.values.keys())
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise HTTPException(
                status_code=400,
                detail=f"Option '{opt.name}' is missing values for: {missing_list}."
            )