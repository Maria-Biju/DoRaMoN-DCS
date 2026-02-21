from fastapi import APIRouter

from app.api.schemas import Scenario, EvaluationResult
from app.engine.evaluate import evaluate_wsm

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Decision Companion System is running",
        "next": "POST /api/evaluate"
    }

@router.post("/api/evaluate", response_model=EvaluationResult)
def evaluate(scenario: Scenario) -> EvaluationResult:
    details = evaluate_wsm(scenario)

    ranked_names = [d.name for d in details]

    return EvaluationResult(
        title=scenario.title,
        ranked_option_names=ranked_names,
        details=details
    )
