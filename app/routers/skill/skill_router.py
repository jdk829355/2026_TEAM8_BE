from fastapi import APIRouter

router = APIRouter(
    prefix="/skill",
    tags=["skill"],
)


@router.patch("/want_to")
def update_want_to():
    return {"message": "update_want_to handler"}


@router.patch("/can_teach")
def update_can_teach():
    return {"message": "update_can_teach handler"}


@router.get("/all")
def get_all_skills():
    return {"message": "get_all_skills handler"}


@router.get("/want_to")
def get_want_to_skills():
    return {"message": "get_want_to_skills handler"}


@router.get("/can_teach")
def get_can_teach_skills():
    return {"message": "get_can_teach_skills handler"}
