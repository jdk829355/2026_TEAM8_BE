import uuid

from sqlalchemy.orm import Session

from app.models.user_models import User


class UserRepository:
    def get_user_by_id(self, db: Session, user_id: uuid.UUID) -> User | None:
        """유저 ID로 유저 조회"""
        return db.query(User).filter(User.id == user_id).first()

    def update_user(self, db: Session, user_id: uuid.UUID, payload: dict) -> User | None:
        """유저 정보 업데이트"""
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None

        for key, value in payload.items():
            if key == "id":
                continue
            if hasattr(user, key):
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
