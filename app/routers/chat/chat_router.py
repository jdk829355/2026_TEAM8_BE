from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/")
def read_chat() -> str:
    return "chat router"
