from fastapi import APIRouter, HTTPException

from app.api.schemas import Scenario, EvaluationResult
from app.engine.evaluate import evaluate_wsm
from app.api.validators import validate_scenario

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Decision Companion System is running",
        "next": "POST /api/evaluate"
    }

@router.post("/api/evaluate", response_model=EvaluationResult)
def evaluate(scenario: Scenario) -> EvaluationResult:
    validate_scenario(scenario)

    try:
        details, filtered_out, companion, sensitivity = evaluate_wsm(scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    ranked_names = [d.name for d in details]

    return EvaluationResult(
        title=scenario.title,
        ranked_option_names=ranked_names,
        details=details,
        filtered_out=filtered_out,
        companion_insight=companion,
        sensitivity=sensitivity
    )