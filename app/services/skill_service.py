from uuid import UUID
from sqlalchemy.orm import Session

from app.repositories.skill_repository import SkillRepository
from app.schemas.skill_schema import (
    WantToLearnRequest,
    CanToTeachRequest,
    ViewAllSkillsResponse,
    ViewWantToLearnResponse,
    ViewCanToTeachResponse,
    EditWantToLearnRequest,
    EditCanToTeachRequest,
)
from app.models.skill_models import Skill, Want, CanTeach


class SkillService:
    def __init__(self, repo: SkillRepository):
        self.repo = repo

    def create_skill(self, db: Session, skill_name: str) -> Skill:
        skill_list = self.repo.search_skill(db, skill_name)
        for skill in skill_list:
            if skill.name.lower() == skill_name.lower():
                return skill
        return self.repo.create_skill(db, skill_name)

    def add_want_to_learn(
        self, db: Session, user_id: UUID, request: WantToLearnRequest
    ) -> ViewWantToLearnResponse:
        learning_skills = []
        for skill_name in request.learning_skill:
            skill = self.create_skill(db, skill_name)
            self.repo.create_want(db, user_id, skill.id)
            learning_skills.append(skill.name)

        return ViewWantToLearnResponse(learning_skill=learning_skills)

    def add_can_teach(
        self, db: Session, user_id: UUID, request: CanToTeachRequest
    ) -> ViewCanToTeachResponse:
        teaching_skills = []
        for skill_name in request.teaching_skill:
            skill = self.create_skill(db, skill_name)
            self.repo.create_can_teach(db, user_id, skill.id)
            teaching_skills.append(skill.name)

        return ViewCanToTeachResponse(teaching_skill=teaching_skills)

    def get_all_skills(self, db: Session, user_id: UUID) -> ViewAllSkillsResponse:
        learning_skills_obj = self.repo.get_learning_skills_by_user(db, user_id)
        teaching_skills_obj = self.repo.get_teaching_skills_by_user(db, user_id)

        learning_skills = [skill.name for skill in learning_skills_obj]
        teaching_skills = [skill.name for skill in teaching_skills_obj]

        return ViewAllSkillsResponse(
            teaching_skill=teaching_skills, learning_skill=learning_skills
        )

    def get_want_to_learn(self, db: Session, user_id: UUID) -> ViewWantToLearnResponse:
        learning_skills_obj = self.repo.get_learning_skills_by_user(db, user_id)
        learning_skills = [skill.name for skill in learning_skills_obj]
        return ViewWantToLearnResponse(learning_skill=learning_skills)

    def get_can_teach(self, db: Session, user_id: UUID) -> ViewCanToTeachResponse:
        teaching_skills_obj = self.repo.get_teaching_skills_by_user(db, user_id)
        teaching_skills = [skill.name for skill in teaching_skills_obj]
        return ViewCanToTeachResponse(teaching_skill=teaching_skills)

    def edit_want_to_learn(
        self, db: Session, user_id: UUID, request: EditWantToLearnRequest
    ) -> ViewWantToLearnResponse:
        # Delete all existing wants
        wants = db.query(Want).filter(Want.user_id == user_id).all()
        for want in wants:
            self.repo.delete_want(db, user_id, want.skill_id)

        # Add new wants
        return self.add_want_to_learn(
            db, user_id, WantToLearnRequest(learning_skill=request.learning_skill)
        )

    def edit_can_teach(
        self, db: Session, user_id: UUID, request: EditCanToTeachRequest
    ) -> ViewCanToTeachResponse:
        # Delete all existing can teaches
        can_teaches = db.query(CanTeach).filter(CanTeach.user_id == user_id).all()
        for can_teach in can_teaches:
            self.repo.delete_can_teach(db, user_id, can_teach.skill_id)

        # Add new can teaches
        return self.add_can_teach(
            db, user_id, CanToTeachRequest(teaching_skill=request.teaching_skill)
        )

    def delete_want_to_learn(
        self, db: Session, user_id: UUID, skill_name: str
    ) -> bool:
        skill = self.repo.get_skill_by_name(db, skill_name)
        if skill is None:
            return False
        return self.repo.delete_want(db, user_id, skill.id)

    def delete_can_teach(self, db: Session, user_id: UUID, skill_name: str) -> bool:
        skill = self.repo.get_skill_by_name(db, skill_name)
        if skill is None:
            return False
        return self.repo.delete_can_teach(db, user_id, skill.id)

    def search_skills(self, db: Session, keyword: str) -> list[Skill]:
        return self.repo.search_skill(db, keyword)

    def get_all_available_skills(self, db: Session) -> list[Skill]:
        return self.repo.get_skill_list(db)
