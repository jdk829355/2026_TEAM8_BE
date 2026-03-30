from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_models import User


class AuthRepository:
    def create_user(self, db: Session, payload: dict):
        user = User(**payload)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_id(self, db: Session, user_id: UUID) -> User|None:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> User|None:
        return db.query(User).filter(User.email == email).first()

    def update_user_verification(self, db: Session, user_id: UUID, is_verified: bool) -> User|None:
        user = self.get_user_by_id(db, user_id)
        if user is None:
            return None

        user.is_verified = is_verified  # type: ignore
        db.commit()
        db.refresh(user)
        return user

    def is_email_duplicated(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first() is not None