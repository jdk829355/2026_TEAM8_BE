from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_matching_service
from app.dependencies.database import get_db
from app.realtime.channels import user_event
from app.schemas.matching_schema import AcceptMatchingRequest
from app.services.matching_service import MatchingService
from app.realtime.publisher import publisher

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
async def accept_matching(
    accept: AcceptMatchingRequest,
    matching_request_id: str,
    service: MatchingService = Depends(get_matching_service),
    db: Session = Depends(get_db),
):
    try:
        matching_request_uuid = UUID(matching_request_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="invalid matching_request_id"
        ) from exc

    if accept.accept:
        try:
            result = service.accept_matching_request(
                db=db,
                matching_request_id=matching_request_uuid,
            )
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=500, detail="failed to accept matching request"
            ) from exc

        await publisher.publish(user_event(str(result["user_id"])), result)
        await publisher.publish(user_event(str(result["to_user_id"])), result)
    else:
        is_deleted = service.reject_matching_request(
            db=db,
            matching_request_id=matching_request_uuid,
        )
        if not is_deleted:
            raise HTTPException(status_code=404, detail="matching request not found")
    return
