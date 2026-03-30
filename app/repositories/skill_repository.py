from uuid import UUID

from sqlalchemy.orm import Session

from app.models.skill_models import CanTeach, Skill, Want


class SkillRepository:
    def create_skill(self, db: Session, name: str) -> Skill:
        skill = Skill(name=name)
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

    def search_skill(self, db: Session, keyword: str) -> list[Skill]:
        pattern = f"%{keyword.strip()}%"
        return (
            db.query(Skill)
            .filter(Skill.name.ilike(pattern))
            .order_by(Skill.name.asc())
            .all()
        )