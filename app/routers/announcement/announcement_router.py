from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_announcement_service
from app.core.verify_jwt import get_current_user_id
from app.dependencies.database import get_db
from app.schemas.announcement_schema import CreateAnnounceRequest
from app.services.announcement_service import AnnouncementService

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
def create_announcement(create_announcement_request: CreateAnnounceRequest, user_id: str = Depends(get_current_user_id), service: AnnouncementService = Depends(get_announcement_service), db = Depends(get_db))->str:
    try:
        announcement = service.create_announcement(db=db, payload=create_announcement_request, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return str(announcement.id)


@router.patch("/{announcement_id}")
def update_announcement(announcement_id, payload: dict):
    _ = announcement_id
    _ = payload
    return {"message": "update_announcement handler"}
