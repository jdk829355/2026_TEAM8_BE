from fastapi import APIRouter

router = APIRouter(
    prefix="/matching",
    tags=["matching"],
)


@router.get("/")
def read_matching() -> str:
    return "matching router"
