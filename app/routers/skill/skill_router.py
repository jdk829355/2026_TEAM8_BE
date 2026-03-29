from fastapi import APIRouter
from app.schemas.auth_schema import SignUpRequest

router = APIRouter(
    prefix="/skill",
    tags=["skill"],
)


@router.get("/")
def read_skills(sign: SignUpRequest):
    sign.email
    return "List of skills"
