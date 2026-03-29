from fastapi import APIRouter

router = APIRouter(
    prefix="/skills",
    tags=["skills"],
)

@router.get("/")
def read_skills():
    return "List of skills"