import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_skill_service
from app.dependencies.database import get_db
from app.core.verify_jwt import get_current_user_id
from app.schemas.skill_schema import (
    CreateSkillRequest,
    WantToLearnRequest,
    CanToTeachRequest,
    SkillItemResponse,
    ViewAllSkillsResponse,
    ViewWantToLearnResponse,
    ViewCanToTeachResponse,
    EditWantToLearnRequest,
    EditCanToTeachRequest,
)
from app.services.skill_service import SkillService

router = APIRouter(
    prefix="/skill",
    tags=["skill"],
)

logger = logging.getLogger(__name__)


@router.post("/want_to", response_model=ViewWantToLearnResponse)
def want_to_learn(
    request: WantToLearnRequest,
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """배우고싶은 것 등록 (WantToLearn)"""
    try:
        result = service.add_want_to_learn(db, user_id, request)
        return result
    except Exception as e:
        logger.error(f"Error while adding want to learn skills: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"배우고싶은 것 등록 실패: {str(e)}"
        )


@router.post("/can_teach", response_model=ViewCanToTeachResponse)
def can_teach(
    request: CanToTeachRequest,
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """가르칠 수 있는 것 등록 (CanToTeach)"""
    try:
        result = service.add_can_teach(db, user_id, request)
        return result
    except Exception as e:
        logger.error(f"Error while adding can teach skills: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"가르칠 수 있는 것 등록 실패: {str(e)}"
        )


@router.get("/all", response_model=ViewAllSkillsResponse)
def view_all_skills(
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """전체 skill 조회 (ViewAllSkills)"""
    try:
        result = service.get_all_skills(db, user_id)
        return result
    except Exception as e:
        logger.error(f"Error while getting all skills: {str(e)}")
        raise HTTPException(status_code=500, detail=f"전체 skill 조회 실패: {str(e)}")


@router.get("/want_to", response_model=ViewWantToLearnResponse)
def view_want_to_learn(
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """배우려는 skill 조회 (ViewWantToLearn)"""
    try:
        result = service.get_want_to_learn(db, user_id)
        return result
    except Exception as e:
        logger.error(f"Error while getting want to learn skills: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"배우려는 skill 조회 실패: {str(e)}"
        )


@router.get("/can_teach", response_model=ViewCanToTeachResponse)
def view_can_teach(
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """가르칠 수 있는 Skill 조회 (ViewCanToTeach)"""
    try:
        result = service.get_can_teach(db, user_id)
        return result
    except Exception as e:
        logger.error(f"Error while getting can teach skills: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"가르칠 수 있는 Skill 조회 실패: {str(e)}"
        )


@router.patch("/want_to", response_model=ViewWantToLearnResponse)
def edit_want_to_learn(
    request: EditWantToLearnRequest,
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """배우고 싶은 스킬 수정 (EditWantToLearn)"""
    try:
        result = service.edit_want_to_learn(db, user_id, request)
        return result
    except Exception as e:
        logger.error(f"Error while editing want to learn skills: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"배우고 싶은 스킬 수정 실패: {str(e)}"
        )


@router.patch("/can_teach", response_model=ViewCanToTeachResponse)
def edit_can_teach(
    request: EditCanToTeachRequest,
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """가르칠 수 있는 스킬 수정 (EditCanToTeach)"""
    try:
        result = service.edit_can_teach(db, user_id, request)
        return result
    except Exception as e:
        logger.error(f"Error while editing can teach skills: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"가르칠 수 있는 스킬 수정 실패: {str(e)}"
        )

# 추가 구현 (정대균)

@router.get("/all_available", response_model=list[SkillItemResponse])
def get_all_available_skills(
    keyword: str | None = None,
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
):
    try:
        skills = service.get_all_available_skills_by_keyword(db, keyword)
        return [
            SkillItemResponse(name=skill.name, category=skill.category) # type: ignore
            for skill in skills
        ]
    except Exception as e:
        logger.error(f"Error while getting available skills: {str(e)}")
        raise HTTPException(status_code=500, detail=f"전체 skill 조회 실패: {str(e)}")


@router.post("", response_model=SkillItemResponse)
def create_skill(
    request: CreateSkillRequest,
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    _: UUID = Depends(get_current_user_id),  # 회원만 추가하도록
):
    try:
        skill = service.create_skill_entry(db, request.name, request.category)
        return SkillItemResponse(name=skill.name, category=skill.category) # type: ignore
    except Exception as e:
        logger.error(f"Error while creating skill: {str(e)}")
        raise HTTPException(status_code=500, detail=f"skill 추가 실패: {str(e)}")


@router.get("/categories", response_model=list[str])
def get_skill_categories(
    service: SkillService = Depends(get_skill_service),
    db: Session = Depends(get_db),
    keyword: str | None = None,
):
    try:
        return service.get_skill_categories(db, keyword)
    except Exception as e:
        logger.error(f"Error while getting skill categories: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"category 목록 조회 실패: {str(e)}"
        )
