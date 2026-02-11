from fastapi import APIRouter

router = APIRouter(prefix="/scoring", tags=["scoring"])


@router.get("/")
def scoring_info():
    return {
        "message": "Scoring endpoint not implemented yet"
    }
