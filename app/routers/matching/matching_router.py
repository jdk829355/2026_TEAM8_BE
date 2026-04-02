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
    ViewDetailMatchingResponse,
    UpdateMatchingRequest,
    UpdateMatchingResponse
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

# app/routers/matching/matching_router.py

@router.get("/my", response_model=ViewMyMatchingListResponse)
async def get_my_matching(
    user_id: UUID = Depends(get_current_user_id), 
    service: MatchingService = Depends(get_matching_service), 
    db: Session = Depends(get_db)
):
    try:
        matchings = service.get_my_matchings(db=db, user_id=user_id)
        items = []
        
        for match in matchings:
            items.append(
                MatchingItem(
                    matching_id=str(match.matching_id),  
                    name=match.name,
                    # 만약 리포지토리에서 skill_name으로 가져왔다면 match.skill_name 사용
                    teaching_skill=match.skill_name if hasattr(match, 'skill_name') else "N/A",
                    learning_skill="상세보기에서 확인", # 리스트에서 배우는 스킬까지 가져오려면 조인이 더 복잡해지므로 일단 고정값
                    status="ACTIVE" # Teach 테이블의 status를 가져와서 써도 됩니다.
                )
            )

        return ViewMyMatchingListResponse(items=items)
    except Exception as exc:
        logger.exception("failed to get my matchings " + str(exc))
        raise HTTPException(status_code=500, detail="failed to get my matchings") from exc


@router.get("/{id}", response_model=ViewDetailMatchingResponse)
async def get_matching_detail(
    id: str,
    user_id: UUID = Depends(get_current_user_id), # 현재 로그인한 유저 ID
    service: MatchingService = Depends(get_matching_service),
    db: Session = Depends(get_db)
):
    logger = logging.getLogger(__name__)

    try:
        matching_uuid = UUID(id) # 변수명 중복 방지를 위해 matching_uuid로 변경
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="invalid id") from exc

    try:
        # 서비스 호출 시 user_id를 추가로 전달합니다.
        result = service.get_matching_detail(
            db=db,
            id=matching_uuid,
            current_user_id=user_id 
        )
        return ViewDetailMatchingResponse(
            opponent_name=result["opponent_name"],
            teaching_skill=result["teaching_skill"],
            learning_skill=result["learning_skill"],
            opponent_id=result["opponent_id"],
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
        if result is None:
            raise HTTPException(status_code=500, detail="failed to reject matching request")
        await publisher.publish(user_event(str(result["user_id"])), result)
        await publisher.publish(user_event(str(result["to_user_id"])), result)
    return


# app/routers/matching/matching_router.py

@router.patch("/{matching_id}", response_model=UpdateMatchingResponse)
async def update_matching(
    matching_id: str,
    request_data: UpdateMatchingRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: MatchingService = Depends(get_matching_service),
    db: Session = Depends(get_db)
):
    try:
        matching_uuid = UUID(matching_id)
        result = service.update_matching_status(
            db=db, 
            matching_id=matching_uuid, 
            user_id=user_id, 
            data=request_data
        )
        return UpdateMatchingResponse(
            name=result["name"],
            matching_status=result["matching_status"]
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Update failed")
