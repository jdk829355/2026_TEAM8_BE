from fastapi import APIRouter

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)


@router.get("/")
def read_todo() -> str:
    return "todo router"
