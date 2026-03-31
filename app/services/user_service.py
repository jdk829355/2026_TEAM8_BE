import uuid
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.repositories.skill_repository import SkillRepository
from app.schemas.user_schema import EditMyProfileRequest, SearchUserProfileResponse


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.skill_repo = SkillRepository()

    def get_user_profile(
        self, db: Session, user_id: uuid.UUID
    ) -> SearchUserProfileResponse | None:
        """유저 프로필 조회 (SearchUserProfile)"""
        user = self.repo.get_user_by_id(db, user_id)
        if user is None:
            return None

        # Skill 저장소에서 teaching_skills, learning_skills 조회
        teaching_skills_obj = self.skill_repo.get_teaching_skills_by_user(db, user_id)
        learning_skills_obj = self.skill_repo.get_learning_skills_by_user(db, user_id)

        teaching_skills = [skill.name for skill in teaching_skills_obj]
        learning_skills = [skill.name for skill in learning_skills_obj]

        return SearchUserProfileResponse(
            name=user.name,
            email=user.email,
            teaching_skills=teaching_skills,
            learning_skills=learning_skills,
        )

    def update_my_profile(
        self, db: Session, user_id: uuid.UUID, request: EditMyProfileRequest
    ) -> SearchUserProfileResponse | None:
        """내 정보 수정 (EditMyProfile)"""
        payload = {
            "name": request.name,
            "description": request.description,
        }
        user = self.repo.update_user(db, user_id, payload)
        if user is None:
            return None

        # 업데이트된 유저의 프로필 반환
        return self.get_user_profile(db, user_id)