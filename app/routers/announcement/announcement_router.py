from fastapi import APIRouter

router = APIRouter(
    prefix="/announcement",
    tags=["announcement"],
)


@router.get("/all")
def get_all_announcements():
    return {"message": "get_all_announcements handler"}


@router.get("/detail/{announcement_id}")
def get_announcement_detail(announcement_id):
    _ = announcement_id
    return {"message": "get_announcement_detail handler"}


@router.post("")
def create_announcement(payload: dict):
    _ = payload
    return {"message": "create_announcement handler"}


@router.patch("/{announcement_id}")
def update_announcement(announcement_id, payload: dict):
    _ = announcement_id
    _ = payload
    return {"message": "update_announcement handler"}
