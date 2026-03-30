from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_matching_service
from app.dependencies.database import get_db
from app.realtime.channels import user_event
from app.schemas.matching_schema import AcceptMatchingRequest
from app.services.matching_service import MatchingService
from app.realtime.publisher import publisher
from app.schemas.chat_schema import WSMessageType

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

@router.post("/{matching_request_id}/accept")
async def accept_matching(accept: AcceptMatchingRequest, matching_request_id: str, service: MatchingService = Depends(get_matching_service), db: Session = Depends(get_db)):
    if accept.accept:
        result = service.accept_matching_request(db=db, matching_request_id=UUID(matching_request_id))

        await publisher.publish(user_event(result["user_id"]), result)
        await publisher.publish(user_event(result["to_user_id"]), result)
    else:
        service.reject_matching_request(db=db, matching_request_id=UUID(matching_request_id))
    return
