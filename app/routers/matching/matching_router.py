import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_matching_service
from app.core.verify_jwt import get_current_user_id
from app.dependencies.database import get_db
from app.realtime.channels import user_event
from app.schemas.matching_schema import AcceptMatchingRequest, MatchingRequestsResponse
from app.schemas.matching_schema import (
    MatchingItem,
    ViewMyMatchingListResponse,
    ViewDetailMatchingResponse
)
from app.services.matching_service import MatchingService
from app.realtime.publisher import publisher

router = APIRouter(
    prefix="/matching",
    tags=["matching"],
)

@router.get("/requests", response_model = MatchingRequestsResponse)
async def get_matching_requests(user_id: UUID = Depends(get_current_user_id), service: MatchingService = Depends(get_matching_service), db: Session = Depends(get_db)):
    logger = logging.getLogger(__name__)
    try:
        result = service.get_matching_request(db=db, user_id=user_id)
        return result
    except Exception as exc:
        logger.exception("failed to get matching requests"+str(exc))
        raise HTTPException(status_code=500, detail="failed to get matching requests") from exc

@router.get("/all", response_model=List[MatchingItem])
async def get_all_matchings(service: MatchingService = Depends(get_matching_service),
    db: Session = Depends(get_db)
):
    
    logger = logging.getLogger(__name__)
    try:
        result = service.get_all_matching(db=db)
        items = [
            MatchingItem(
                matching_id=str(m.matching_id),
                name=m.name,
                teaching_skill=m.teaching_skill,
                learning_skill=m.learning_skill,
                status=m.status
            )
            for m in result
        ]

        return items
    except Exception as exc:
        logger.exception("failed to get all matching"+str(exc))
        raise HTTPException(status_code=500, detail="failed to get all matchings") from exc


@router.get("/my", response_model = ViewMyMatchingListResponse)
async def get_my_matching(user_id: UUID = Depends(get_current_user_id), service: MatchingService = Depends(get_matching_service), db: Session = Depends(get_db))
    logger = logging.getLogger(__name__)

    try:
        matchings = service.get_my_matchings(db=db, user_id=user_id)
        items = [
            MatchingItem(
                matching_id=str(match.matching_id),  
                name=match.name,
                teaching_skill=match.teaching_skill,
                learning_skill=match.learning_skill,
                status=match.status
            )
            for match in matchings
        ]

        return ViewMyMatchingListResponse(items=items)
    except Exception as exc:
        logger.exception("failed to get my matchings " + str(exc))
        raise HTTPException(status_code=500, detail="failed to get my matchings") from exc


@router.get("/{id}", response_model= ViewDetailMatchingResponse)
async def get_matching_detail(
    id: str,
    service: MatchingService = Depends(get_matching_service),
    db: Session = Depends(get_db)
):
    logger = logging.getLogger(__name__)

    try:
        matching_id = UUID(id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="invalid id") from exc

    try:
        result = service.get_matching_detail(
            db=db,
            matching_id=matching_id
        )
        return ViewDetailMatchingResponse(
            opponent_name=result.opponent_name,
            teaching_skill=result.teaching_skill,
            learning_skill=result.learning_skill,
            opponent_id=str(result.opponent_id) 
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("failed to get matching detail " + str(exc))
        raise HTTPException(status_code=500, detail="failed to get matching detail") from exc


@router.post("/{matching_request_id}/accept")
async def accept_matching(
    accept: AcceptMatchingRequest,
    matching_request_id: str,
    service: MatchingService = Depends(get_matching_service),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
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
        is_deleted, result = service.reject_matching_request(
            db=db,
            matching_request_id=matching_request_uuid,
        )
        if not is_deleted:
            raise HTTPException(status_code=404, detail="matching request not found")
        await publisher.publish(user_event(str(result["user_id"])), result)
        await publisher.publish(user_event(str(result["to_user_id"])), result)
    return

