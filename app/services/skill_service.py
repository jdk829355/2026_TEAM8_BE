from uuid import UUID
from sqlalchemy.orm import Session

from app.repositories.skill_repository import SkillRepository
from app.schemas.skill_schema import (
    WantToLearnRequest,
    CanToTeachRequest,
    SkillItem,
    ViewAllSkillsResponse,
    ViewWantToLearnResponse,
    ViewCanToTeachResponse,
    EditWantToLearnRequest,
    EditCanToTeachRequest,
)
from app.models.skill_models import Skill, Want, CanTeach
from app.services.ai_service import AiService


class SkillService:
    def __init__(self, repo: SkillRepository, ai_service: AiService):
        self.repo = repo
        self.ai_service = ai_service

    def create_skill(
        self,
        db: Session,
        skill_name: str,
        category: str = "general",
    ) -> Skill:
        skill_list = self.repo.search_skill(db, skill_name)
        for skill in skill_list:
            if (
                skill.name.lower() == skill_name.lower()
                and skill.category.lower() == category.lower()
            ):
                return skill
        return self.repo.create_skill(db, skill_name, category)

    def add_want_to_learn(
        self, db: Session, user_id: UUID, request: WantToLearnRequest
    ) -> ViewWantToLearnResponse:
        want_to_skills: list[SkillItem] = []
        for item in request.want_to_skill:
            skill = self.create_skill(db, item.name, item.category)
            self.repo.create_want(db, user_id, skill.id)  # type: ignore
            want_to_skills.append(
                SkillItem(name=skill.name, category=skill.category),  # type: ignore
            )

        return ViewWantToLearnResponse(want_to_skill=want_to_skills)

    def add_can_teach(
        self, db: Session, user_id: UUID, request: CanToTeachRequest
    ) -> ViewCanToTeachResponse:
        can_teach_skills: list[SkillItem] = []
        for item in request.can_teach_skill:
            skill = self.create_skill(db, item.name, item.category)
            self.repo.create_can_teach(db, user_id, skill.id)  # type: ignore
            can_teach_skills.append(
                SkillItem(name=skill.name, category=skill.category),  # type: ignore
            )

        return ViewCanToTeachResponse(can_teach_skill=can_teach_skills)

    def get_all_skills(self, db: Session, user_id: UUID) -> ViewAllSkillsResponse:
        want_to_skills_obj = self.repo.get_learning_skills_by_user(db, user_id)
        can_teach_skills_obj = self.repo.get_teaching_skills_by_user(db, user_id)

        want_to_skills = [
            SkillItem(name=skill.name, category=skill.category)  # type: ignore
            for skill in want_to_skills_obj
        ]
        can_teach_skills = [
            SkillItem(name=skill.name, category=skill.category)  # type: ignore
            for skill in can_teach_skills_obj
        ]

        return ViewAllSkillsResponse(
            can_teach_skill=can_teach_skills,  # type: ignore
            want_to_skill=want_to_skills,  # type: ignore
        )

    def get_want_to_learn(self, db: Session, user_id: UUID) -> ViewWantToLearnResponse:
        want_to_skills_obj = self.repo.get_learning_skills_by_user(db, user_id)
        want_to_skills = [
            SkillItem(name=skill.name, category=skill.category)  # type: ignore
            for skill in want_to_skills_obj
        ]
        return ViewWantToLearnResponse(want_to_skill=want_to_skills)

    def get_can_teach(self, db: Session, user_id: UUID) -> ViewCanToTeachResponse:
        can_teach_skills_obj = self.repo.get_teaching_skills_by_user(db, user_id)
        can_teach_skills = [
            SkillItem(name=skill.name, category=skill.category)  # type: ignore
            for skill in can_teach_skills_obj
        ]
        return ViewCanToTeachResponse(can_teach_skill=can_teach_skills)

    def edit_want_to_learn(
        self, db: Session, user_id: UUID, request: EditWantToLearnRequest
    ) -> ViewWantToLearnResponse:
        # Delete all existing wants
        wants = db.query(Want).filter(Want.user_id == user_id).all()
        for want in wants:
            self.repo.delete_want(db, user_id, want.skill_id)  # type: ignore

        # Add new wants
        return self.add_want_to_learn(
            db,
            user_id,
            WantToLearnRequest(want_to_skill=request.want_to_skill),
        )

    def edit_can_teach(
        self, db: Session, user_id: UUID, request: EditCanToTeachRequest
    ) -> ViewCanToTeachResponse:
        # Delete all existing can teaches
        can_teaches = db.query(CanTeach).filter(CanTeach.user_id == user_id).all()
        for can_teach in can_teaches:
            self.repo.delete_can_teach(db, user_id, can_teach.skill_id)  # type: ignore

        # Add new can teaches
        return self.add_can_teach(
            db,
            user_id,
            CanToTeachRequest(can_teach_skill=request.can_teach_skill),
        )

    def delete_want_to_learn(self, db: Session, user_id: UUID, skill_name: str) -> bool:
        skill = self.repo.get_skill_by_name(db, skill_name)
        if skill is None:
            return False
        return self.repo.delete_want(db, user_id, skill.id)  # type: ignore

    def delete_can_teach(self, db: Session, user_id: UUID, skill_name: str) -> bool:
        skill = self.repo.get_skill_by_name(db, skill_name)
        if skill is None:
            return False
        return self.repo.delete_can_teach(db, user_id, skill.id)  # type: ignore

    # 추가 구현 (정대균)
    def search_skills(self, db: Session, keyword: str) -> list[Skill]:
        return self.repo.search_skill(db, keyword)

    def get_all_available_skills(self, db: Session) -> list[Skill]:
        return self.repo.get_skill_list(db)

    def create_skill_entry(self, db: Session, name: str, category: str) -> Skill:
        existing = self.repo.get_skill_by_name_and_category(db, name, category)
        if existing is not None:
            return existing
        embedding = self.ai_service.encode_skill_name(name)
        return self.repo.create_skill(db, name, category, embedding)

    def get_all_available_skills_by_keyword(
        self,
        db: Session,
        keyword: str | None,
    ) -> list[Skill]:
        return self.repo.get_skill_list_by_keyword(db, keyword)

    def get_skill_categories(
        self, db: Session, keyword: str | None = None
    ) -> list[str]:
        return self.repo.get_categories(db, keyword)
