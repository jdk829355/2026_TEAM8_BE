from uuid import UUID

from sqlalchemy.orm import Session

from app.models.skill_models import CanTeach, Skill, Want


class SkillRepository:
    def create_skill(self, db: Session, name: str, category: str = "general") -> Skill:
        skill = Skill(name=name, category=category)
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return skill

    def delete_skill(self, db: Session, skill_id: UUID) -> bool:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if skill is None:
            return False

        db.delete(skill)
        db.commit()
        return True

    def create_want(self, db: Session, user_id: UUID, skill_id: UUID) -> Want:
        want = (
            db.query(Want)
            .filter(
                Want.user_id == user_id,
                Want.skill_id == skill_id,
            )
            .first()
        )
        if want is not None:
            return want

        want = Want(user_id=user_id, skill_id=skill_id)
        db.add(want)
        db.commit()
        db.refresh(want)
        return want

    def create_can_teach(self, db: Session, user_id: UUID, skill_id: UUID) -> CanTeach:
        can_teach = (
            db.query(CanTeach)
            .filter(
                CanTeach.user_id == user_id,
                CanTeach.skill_id == skill_id,
            )
            .first()
        )
        if can_teach is not None:
            return can_teach

        can_teach = CanTeach(user_id=user_id, skill_id=skill_id)
        db.add(can_teach)
        db.commit()
        db.refresh(can_teach)
        return can_teach

    def delete_want(self, db: Session, user_id: UUID, skill_id: UUID) -> bool:
        want = (
            db.query(Want)
            .filter(
                Want.user_id == user_id,
                Want.skill_id == skill_id,
            )
            .first()
        )
        if want is None:
            return False

        db.delete(want)
        db.commit()
        return True

    def delete_can_teach(self, db: Session, user_id: UUID, skill_id: UUID) -> bool:
        can_teach = (
            db.query(CanTeach)
            .filter(
                CanTeach.user_id == user_id,
                CanTeach.skill_id == skill_id,
            )
            .first()
        )
        if can_teach is None:
            return False

        db.delete(can_teach)
        db.commit()
        return True

    def get_skill_list(self, db: Session) -> list[Skill]:
        return db.query(Skill).order_by(Skill.name.asc()).all()

    def get_skill_list_by_keyword(
        self, db: Session, keyword: str | None
    ) -> list[Skill]:
        query = db.query(Skill)
        if keyword is not None and keyword.strip():
            pattern = f"%{keyword.strip()}%"
            query = query.filter(Skill.name.ilike(pattern) | Skill.category.ilike(pattern))
        return query.order_by(Skill.name.asc()).all()

    def search_skill(self, db: Session, keyword: str) -> list[Skill]:
        pattern = f"%{keyword.strip()}%"
        return (
            db.query(Skill)
            .filter(Skill.name.ilike(pattern))
            .order_by(Skill.name.asc())
            .all()
        )

    def get_learning_skills_by_user(self, db: Session, user_id: UUID) -> list[Skill]:
        """Get all learning skills for a user using join"""
        return (
            db.query(Skill)
            .join(Want, Skill.id == Want.skill_id)
            .filter(Want.user_id == user_id)
            .order_by(Skill.name.asc())
            .all()
        )

    def get_teaching_skills_by_user(self, db: Session, user_id: UUID) -> list[Skill]:
        return (
            db.query(Skill)
            .join(CanTeach, Skill.id == CanTeach.skill_id)
            .filter(CanTeach.user_id == user_id)
            .order_by(Skill.name.asc())
            .all()
        )

    def get_skill_by_name(self, db: Session, name: str) -> Skill | None:
        return db.query(Skill).filter(Skill.name.ilike(name)).first()

    def get_skill_by_name_and_category(
        self,
        db: Session,
        name: str,
        category: str,
    ) -> Skill | None:
        return (
            db.query(Skill)
            .filter(
                Skill.name.ilike(name),
                Skill.category.ilike(category),
            )
            .first()
        )

    def get_categories(self, db: Session, keyword: str | None) -> list[str]:
        pattern = f"%{keyword.strip()}%" if keyword is not None and keyword.strip() else None
        query = db.query(Skill.category).distinct().order_by(Skill.category.asc())
        if pattern:
            query = query.filter(Skill.category.ilike(pattern))
        categories = (
            query.all()
        )
        return [category for (category,) in categories]
