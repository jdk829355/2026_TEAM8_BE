from fastapi import APIRouter

router = APIRouter(
    prefix="/announcement",
    tags=["announcement"],
)


@router.get("/")
def read_announcement() -> str:
    return "announcement router"
