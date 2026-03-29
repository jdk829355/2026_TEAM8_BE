from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/")
def read_auth() -> str:
    return "auth router"
