from uuid import UUID

from sqlalchemy.orm import Session

from app.models.announcement_models import Announcement


class AnnouncementRepository:
    def get_all(self, db: Session):
        return db.query(Announcement).all()

    def get_by_id(self, db: Session, announcement_id: UUID):
        return db.query(Announcement).filter(Announcement.id == announcement_id).first()

    def create(self, db: Session, payload: dict):
        announcement = Announcement(**payload)
        db.add(announcement)
        db.commit()
        db.refresh(announcement)
        return announcement

    def update(self, db: Session, announcement: Announcement, payload: dict):
        for key, value in payload.items():
            if hasattr(announcement, key):
                setattr(announcement, key, value)

        db.commit()
        db.refresh(announcement)
        return announcement

    def delete(self, db: Session, announcement: Announcement):
        db.delete(announcement)
        db.commit()