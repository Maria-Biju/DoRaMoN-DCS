from fastapi import APIRouter
from app.api.schemas import Scenario, EvaluationResult


router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Decision Companion System is running",
        "next": "POST /api/evaluate (coming soon)"
    }
