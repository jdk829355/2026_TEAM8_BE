from datetime import datetime
from typing import Any
from uuid import UUID
from app.models import User

from sqlalchemy.orm import Session, aliased

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

    def create_matching(
        self, db: Session, announcement_id: UUID, host_id: UUID, guest_id: UUID
    ) -> Matching | None:

        announcement = (
            db.query(Announcement).filter(Announcement.id == announcement_id).first()
        )
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
                teacher_id=announcement.user_id,
                skill_id=announcement.can_teach_skill,
                matching_id=matching.id,
                status="ACTIVE",
            ),
            Teach(
                teacher_id=guest_id,
                skill_id=announcement.want_to_skill,
                matching_id=matching.id,
                status="ACTIVE",
            ),
        }
        for t in teach:
            db.add(t)
        db.commit()
        return matching

    def create_matching_from_request(
        self,
        db: Session,
        matching_request_id: UUID,
    ) -> tuple[UUID, UUID, UUID, UUID] | None:
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

        announcement = (
            db.query(Announcement)
            .filter(Announcement.id == chatroom.announcement_id)
            .first()
        )
        if announcement is None or announcement.user_id is None:
            return None

        host_user_id = announcement.user_id
        guest_user_id = (
            matching_request.from_user_id
            if matching_request.from_user_id != host_user_id # type: ignore
            else matching_request.to_user_id
        )
        if guest_user_id is None:
            return None

        try:
            name = f"이름 없는 매칭 {datetime.now().strftime('%Y%m%d')}"
            matching = Matching(name=name)
            db.add(matching)
            db.flush()

            db.add(
                Teach(
                    teacher_id=host_user_id,
                    skill_id=announcement.can_teach_skill,
                    matching_id=matching.id,
                    status="ACTIVE",
                )
            )
            db.add(
                Teach(
                    teacher_id=guest_user_id,
                    skill_id=announcement.want_to_skill,
                    matching_id=matching.id,
                    status="ACTIVE",
                )
            )

            chatroom.matching_id = matching.id  # type: ignore
            db.delete(matching_request)
            db.commit()
        except Exception:
            db.rollback()
            raise

        return (matching.id, host_user_id, guest_user_id, announcement.id)  # type: ignore

    def matching_request_info(self, db: Session, matching_request_id: UUID) -> dict[str, Any] | None:
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

        announcement = (
            db.query(Announcement)
            .filter(Announcement.id == chatroom.announcement_id)
            .first()
        )
        if announcement is None or announcement.user_id is None:
            return None

        host_user_id = announcement.user_id
        guest_user_id = (
            matching_request.from_user_id
            if matching_request.from_user_id != host_user_id  # type: ignore
            else matching_request.to_user_id
        )
        if guest_user_id is None:
            return None
        return {"host_user_id": host_user_id, "guest_user_id": guest_user_id}

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

    def get_matching_request(self, db: Session, user_id: UUID) -> tuple[list[tuple[MatchingRequest, str]], list[tuple[MatchingRequest, str]]]:


        matching_request_send = (
            db.query(MatchingRequest, User.name.label("opponent_name"))
            .filter(MatchingRequest.from_user_id == user_id)
            .join(User, User.id == MatchingRequest.to_user_id)
            .all()
        )
        matching_reqeust_receive = (
            db.query(MatchingRequest, User.name.label("opponent_name"))
            .filter(MatchingRequest.to_user_id == user_id)
            .join(User, User.id == MatchingRequest.from_user_id)
            .all()
        )
        return matching_request_send, matching_reqeust_receive # type: ignore
