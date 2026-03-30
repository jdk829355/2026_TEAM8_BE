from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.announcement_models import Announcement
from app.models.chat_models import Chatroom, MatchingRequest
from app.models.matching_models import Matching, Teach


class MatchingRepository:
    def accept_matching_request(
        self,
        db: Session,
        matching_request_id: UUID,
        matching_id: UUID,
    ) -> Chatroom | None:
        """이미 있는 matching에 대해 matching request를 연결하고 matching request를 삭제하는 로직"

        Args:
            db (Session):
            matching_request_id (UUID):
            matching_id (UUID):

        Returns:
            Chatroom | None:
        """
        matching_request = (
            db.query(MatchingRequest)
            .filter(MatchingRequest.id == matching_request_id)
            .first()
        )
        if matching_request is None:
            return None

        chatroom = (
            db.query(Chatroom).filter(Chatroom.id == matching_request.room_id).first()
        )
        if chatroom is None:
            return None

        chatroom.matching_id = matching_id  # type: ignore
        db.delete(matching_request)
        db.commit()
        db.refresh(chatroom)
        return chatroom
    
    def create_matching(self, db:Session, announcement_id: UUID, host_id: UUID, guest_id: UUID) -> Matching|None:
        

        announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
        if announcement is None:
            return None
        
        # 생성 이름: 이름 없는 매칭 YYYYMMDD
        name = f"이름 없는 매칭 {datetime.now().strftime('%Y%m%d')}"
        
        matching = Matching(name=name)
        db.add(matching)
        db.commit()
        db.refresh(matching)

        teach: set[Teach] = {
            Teach(
                teacher_id = announcement.user_id, 
                skill_id = announcement.can_teach_skill,
                matching_id = matching.id, 
                status = "ACTIVE"
            ),
            Teach(
                teacher_id = guest_id,
                skill_id = announcement.want_skill,
                matching_id = matching.id,
                status = "ACTIVE"
            )
        }
        for t in teach:
            db.add(t)
        db.commit()
        return matching
    

    def reject_matching_request(self, db: Session, matching_request_id: UUID) -> bool:
        matching_request = (
            db.query(MatchingRequest)
            .filter(MatchingRequest.id == matching_request_id)
            .first()
        )
        if matching_request is None:
            return False

        db.delete(matching_request)
        db.commit()
        return True