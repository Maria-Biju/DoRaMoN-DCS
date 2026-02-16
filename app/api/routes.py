from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Decision Companion System is running",
        "next": "POST /api/evaluate (coming soon)"
    }
