import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_user_service
from app.dependencies.database import get_db
from app.core.verify_jwt import get_current_user_id
from app.schemas.user_schema import EditMyProfileRequest, SearchUserProfileResponse
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

logger = logging.getLogger(__name__)


@router.get("/{user_id}/profile", response_model=SearchUserProfileResponse)
def search_user_profile(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db),
):
    """유저 프로필 조회 (SearchUserProfile)"""
    try:
        result = service.get_user_profile(db, user_id)
        if result is None:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error while getting user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"유저 프로필 조회 실패: {str(e)}")


@router.patch("/me", response_model=SearchUserProfileResponse)
def edit_my_profile(
    request: EditMyProfileRequest,
    service: UserService = Depends(get_user_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """내 정보 수정 (EditMyProfile)"""
    try:
        result = service.update_my_profile(db, user_id, request)
        if result is None:
            raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error while updating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"내 정보 수정 실패: {str(e)}")
