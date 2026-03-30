from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.announcement_models import Announcement
from app.models.chat_models import ChatLog, Chatroom, JoinChat, MatchingRequest


class ChatRepository:
    def get_my_chatrooms(self, db: Session, user_id: UUID) -> list[Chatroom]:
        return (
            db.query(Chatroom)
            .join(JoinChat, JoinChat.room_id == Chatroom.id)
            .filter(JoinChat.user_id == user_id)
            .all()
        )

    def get_chat_logs(
        self,
        db: Session,
        room_id: UUID,
        before_timestamp: datetime | None = None,
        limit: int = 50,
    ) -> list[ChatLog]:
        query = db.query(ChatLog).filter(ChatLog.room_id == room_id)
        if before_timestamp is not None:
            query = query.filter(ChatLog.timestamp < before_timestamp)

        logs = query.order_by(ChatLog.timestamp.desc()).limit(limit).all()
        logs.reverse()
        return logs

    def get_received_matching_requests(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[MatchingRequest]:
        return (
            db.query(MatchingRequest)
            .filter(MatchingRequest.to_user_id == user_id)
            .all()
        )

    def get_sent_matching_requests(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[MatchingRequest]:
        return (
            db.query(MatchingRequest)
            .filter(MatchingRequest.from_user_id == user_id)
            .all()
        )

    def create_chatroom(
        self,
        db: Session,
        announcement_id: UUID,
        participant_user_id: UUID,
        name: str,
    ) -> Chatroom | None:
        announcement = (
            db.query(Announcement).filter(Announcement.id == announcement_id).first()
        )
        if announcement is None:
            return None

        chatroom = Chatroom(
            name=name,
            matching_id=None,
            announcement_id=announcement_id,
            user_id=participant_user_id,
        )
        db.add(chatroom)
        db.flush()

        participant_ids = {participant_user_id, announcement.user_id}
        for user_id in participant_ids:
            if user_id is None:
                continue
            db.add(JoinChat(user_id=user_id, room_id=chatroom.id))

        db.commit()
        db.refresh(chatroom)
        return chatroom

    def create_chat_log(
        self,
        db: Session,
        room_id: UUID,
        author_id: UUID,
        content: str,
        timestamp: datetime | None = None,
    ) -> ChatLog:
        chat_log = ChatLog(
            room_id=room_id,
            author_id=author_id,
            content=content,
            timestamp=timestamp or datetime.now(timezone.utc),
            read=False,
        )
        db.add(chat_log)
        db.commit()
        db.refresh(chat_log)
        return chat_log

    def create_matching_request(
        self,
        db: Session,
        from_user_id: UUID,
        room_id: UUID,
    ) -> MatchingRequest | None:
        room = db.query(Chatroom).filter(Chatroom.id == room_id).first()
        if room is None:
            return None

        opponent_row = (
            db.query(JoinChat.user_id)
            .filter(JoinChat.room_id == room_id, JoinChat.user_id != from_user_id)
            .first()
        )
        to_user_id = opponent_row[0] if opponent_row is not None else None


        if to_user_id is None:
            return None

        existing_request = (
            db.query(MatchingRequest)
            .filter(
                MatchingRequest.from_user_id == from_user_id,
                MatchingRequest.to_user_id == to_user_id,
                MatchingRequest.room_id == room_id,
            )
            .first()
        )
        if existing_request is not None:
            return existing_request

        matching_request = MatchingRequest(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            room_id=room_id,
        )
        db.add(matching_request)
        db.commit()
        db.refresh(matching_request)
        return matching_request

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

    def update_chatroom_name(
        self,
        db: Session,
        room_id: UUID,
        name: str,
    ) -> Chatroom | None:
        chatroom = db.query(Chatroom).filter(Chatroom.id == room_id).first()
        if chatroom is None:
            return None

        chatroom.name = name  # type: ignore
        db.commit()
        db.refresh(chatroom)
        return chatroom

    def mark_messages_as_read(self, db: Session, room_id: UUID, user_id: UUID) -> int:
        logs = (
            db.query(ChatLog)
            .filter(
                ChatLog.room_id == room_id,
                ChatLog.author_id != user_id,
                ChatLog.read.is_(False),
            )
            .all()
        )

        for log in logs:
            log.read = True  # type: ignore

        db.commit()
        return len(logs)
