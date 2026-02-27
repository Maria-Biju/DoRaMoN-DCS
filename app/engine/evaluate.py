from __future__ import annotations

from typing import Dict, List, Tuple, Optional
from app.api.schemas import CompanionInsight
from app.api.schemas import (
    Scenario,
    OptionExplanation,
    FilteredOutOption,
    CompanionInsight,
    SensitivityResult,
    SensitivityTest,
)
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


def _build_why(strengths: List[str], weaknesses: List[str], score: float) -> str:
    """Template-based, human-readable explanation."""
    if not strengths:
        strength_text = "the provided criteria"
    elif len(strengths) == 1:
        strength_text = strengths[0]
    else:
        strength_text = f"{strengths[0]} and {strengths[1]}"

    if not weaknesses:
        weakness_text = "other criteria"
    elif len(weaknesses) == 1:
        weakness_text = weaknesses[0]
    else:
        weakness_text = f"{weaknesses[0]} and {weaknesses[1]}"

    return (
        f"Scored {round(score,4)} mainly due to strong performance on {strength_text}. "
        f"Lower contribution came from {weakness_text}."
    )


def _winner_index(scores: List[float]) -> int:
    return max(range(len(scores)), key=lambda i: scores[i])


def _compute_scores(
    criteria_ids: List[str],
    option_count: int,
    norm_by_criterion: Dict[str, List[float]],
    w_norm: Dict[str, float],
) -> List[float]:
    scores = [0.0] * option_count
    for i in range(option_count):
        total = 0.0
        for cid in criteria_ids:
            total += float(w_norm[cid]) * float(norm_by_criterion[cid][i])
        scores[i] = total
    return scores


def _build_companion_insight(
    ranked: List[OptionExplanation],
    scenario: Scenario,
) -> Optional[CompanionInsight]:
    """
    Part 13 (Companion Insight):
    - closest competitor = runner-up
    - why competitor lost = criteria where runner-up contributed less than winner (top 2)
    """
    if len(ranked) < 2:
        return None

    winner = ranked[0]
    runner = ranked[1]

    # delta = runner - winner; negative means runner underperformed
    deltas: List[Tuple[str, float]] = []
    for c in scenario.criteria:
        w_contrib = float(winner.contributions.get(c.id, 0.0))
        r_contrib = float(runner.contributions.get(c.id, 0.0))
        deltas.append((c.name, r_contrib - w_contrib))

    negatives = [(name, d) for (name, d) in deltas if d < 0]
    negatives.sort(key=lambda x: x[1])  # most negative first

    reasons: List[str] = []
    for name, d in negatives[:2]:
        reasons.append(f"Lower contribution on {name} ({round(d,4)}) compared to {winner.name}")

    if not reasons:
        reasons.append("Scores are very close; small preference changes may flip the ranking.")

    gap = round(float(winner.score) - float(runner.score), 4)
    summary = (
        f"{winner.name} ranked #1. Closest competitor is {runner.name}. "
        f"{runner.name} lost mainly because: " + "; ".join(reasons)
    )

    return CompanionInsight(
        winner=winner.name,
        runner_up=runner.name,
        runner_up_gap=gap,
        runner_up_reasons=reasons,
        summary=summary,
    )


def _build_sensitivity(
    scenario: Scenario,
    option_names: List[str],
    norm_by_criterion: Dict[str, List[float]],
    base_weights_norm: Dict[str, float],
    delta: float = 0.10,
) -> SensitivityResult:
    """
    Part 13 (Sensitivity):
    Increase one weight at a time by +delta, renormalize, recompute winner.
    """
    criteria_ids = [c.id for c in scenario.criteria]

    base_scores = _compute_scores(criteria_ids, len(option_names), norm_by_criterion, base_weights_norm)
    base_winner = option_names[_winner_index(base_scores)]

    tests: List[SensitivityTest] = []
    most_sensitive: Optional[str] = None

    for cid in criteria_ids:
        w2 = dict(base_weights_norm)
        w2[cid] = w2[cid] + delta

        s = sum(w2.values())
        if s == 0:
            continue
        for k in w2:
            w2[k] = w2[k] / s

        scores2 = _compute_scores(criteria_ids, len(option_names), norm_by_criterion, w2)
        winner2 = option_names[_winner_index(scores2)]
        changed = winner2 != base_winner

        tests.append(SensitivityTest(criterion_id=cid, winner_after=winner2, changed=changed))

        if changed and most_sensitive is None:
            most_sensitive = cid

    summary = (
        f"Winner stays the same for all +{int(delta*100)}% single-criterion weight changes."
        if most_sensitive is None
        else f"Winner changes when '{most_sensitive}' weight is increased by +{int(delta*100)}% (then renormalized)."
    )

    return SensitivityResult(
        delta=delta,
        winner=base_winner,
        summary=summary,
        tests=tests,
        most_sensitive_criterion_id=most_sensitive,
    )


def evaluate_wsm(
    scenario: Scenario,
) -> Tuple[
    List[OptionExplanation],
    List[FilteredOutOption],
    Optional[CompanionInsight],
    Optional[SensitivityResult],
]:
    """
    MCDA - Weighted Sum Model (WSM)

    Includes:
    - Part 8: apply constraints before scoring
    - Part 6: strengths/weaknesses/why (template explanations)
    - Part 13: companion insight + sensitivity analysis

    Returns:
      (ranked_explanations, filtered_out, companion_insight, sensitivity)
    """
    if len(scenario.criteria) == 0:
        raise ValueError("At least one criterion is required.")
    if len(scenario.options) < 2:
        raise ValueError("At least two options are required.")

    # Part 8: constraints
    kept_options, filtered_out = apply_constraints(
        criteria=scenario.criteria,
        options=scenario.options,
        constraints=getattr(scenario, "constraints", []) or [],
    )

    if len(kept_options) < 2:
        return [], filtered_out, None, None

    criterion_name: Dict[str, str] = {c.id: c.name for c in scenario.criteria}

    # Normalize weights
    w_raw = {c.id: float(c.weight) for c in scenario.criteria}
    w_norm = renormalize_weights(w_raw)

    # Collect raw numeric values per criterion across kept options
    raw_by_criterion: Dict[str, List[float]] = {c.id: [] for c in scenario.criteria}

    for opt in kept_options:
        for c in scenario.criteria:
            if c.id not in opt.values:
                raise ValueError(f"Option '{opt.name}' missing value for criterion '{c.name}' ({c.id}).")

            v = opt.values[c.id]
            if not isinstance(v, (int, float)):
                raise ValueError(f"Criterion '{c.name}' expects a number (got {type(v).__name__}).")

            raw_by_criterion[c.id].append(float(v))

    # Normalize each criterion into [0,1] based on goal (benefit/cost)
    norm_by_criterion: Dict[str, List[float]] = {}
    for c in scenario.criteria:
        norm_by_criterion[c.id] = normalize_minmax(raw_by_criterion[c.id], c.goal)

    # Compute results with explanations
    results: List[OptionExplanation] = []

    for i, opt in enumerate(kept_options):
        total_score = 0.0
        contributions: Dict[str, float] = {}
        readable_pairs: List[Tuple[str, float]] = []

        for c in scenario.criteria:
            contrib = float(w_norm[c.id]) * float(norm_by_criterion[c.id][i])
            contrib_r = round(contrib, 4)
            contributions[c.id] = contrib_r
            total_score += contrib
            readable_pairs.append((criterion_name[c.id], contrib_r))

        total_score_r = round(total_score, 4)
        strengths = _top_k_contributors(readable_pairs, k=min(2, len(readable_pairs)))
        weaknesses = _bottom_k_contributors(readable_pairs, k=min(2, len(readable_pairs)))
        why = _build_why(strengths, weaknesses, total_score_r)

        results.append(
            OptionExplanation(
                name=opt.name,
                score=total_score_r,
                contributions=contributions,
                strengths=strengths,
                weaknesses=weaknesses,
                why=why,
            )
        )

    # Rank by score descending
    results.sort(key=lambda r: float(r.score), reverse=True)

    # Part 13: companion insight + sensitivity
    companion = _build_companion_insight(results, scenario)
    option_names = [o.name for o in kept_options]
    sensitivity = _build_sensitivity(scenario, option_names, norm_by_criterion, w_norm, delta=0.10)

    return results, filtered_out, companion, sensitivity