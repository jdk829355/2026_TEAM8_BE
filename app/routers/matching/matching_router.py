from fastapi import APIRouter

router = APIRouter(
    prefix="/matching",
    tags=["matching"],
)


@router.get("/all")
def get_all_matchings():
    return {"message": "get_all_matchings handler"}


@router.get("/my")
def get_my_matchings():
    return {"message": "get_my_matchings handler"}


@router.get("/{id}")
def get_matching_detail(id: str):
    _ = id
    return {"message": "get_matching_detail handler"}
