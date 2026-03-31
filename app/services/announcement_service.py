from uuid import UUID

from app.models.announcement_models import Announcement
from app.repositories.announcement_repository import AnnouncementRepository
from app.schemas.announcement_schema import CreateAnnounceRequest


class AnnouncementService:
    def __init__(self, repo: AnnouncementRepository):
        self.repo = repo

    def create_announcement(self, db, payload: CreateAnnounceRequest, user_id: str) -> Announcement:
        payload_dict = payload.model_dump()

        want_to_skill_name = payload_dict.pop("wantToSkill")
        can_teach_skill_name = payload_dict.pop("canTeachSkill")
        want_to_skill_id = self.repo.skill_name_to_id(db, want_to_skill_name)
        can_teach_skill_id = self.repo.skill_name_to_id(db, can_teach_skill_name)
        if want_to_skill_id is None or can_teach_skill_id is None:
            raise ValueError("Invalid skill name")
        

        return self.repo.create(db, {
            "want_to_skill": want_to_skill_id,
            "can_teach_skill": can_teach_skill_id,
            "want_to_message": payload_dict.pop("wantToMessage"),
            "can_teach_message": payload_dict.pop("canTeachMessage"),
            "user_id": UUID(user_id),
            "want_to_difficulty": payload_dict.pop("wantToDifficulty"),
            "can_teach_difficulty": payload_dict.pop("canTeachDifficulty"),
        })
