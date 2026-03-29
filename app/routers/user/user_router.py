from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/{user_id}/profile")
def get_user_profile(user_id: str):
    _ = user_id
    return {"message": "get_user_profile handler"}


@router.patch("/me")
def update_my_profile():
    return {"message": "update_my_profile handler"}
