from uuid import UUID

from sqlalchemy.orm import Session

from app.models.chat_models import MatchingRequest
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat_schema import ChatLogResponse, ChatRoomInfo, WSMessageType, WSSubscribeMessage


class ChatService:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    def handle_ws_message(self, db: Session, event: dict):
        match event["type"]:
            case WSMessageType.JOIN_CHAT:
                return event
            case WSMessageType.SEND_MESSAGE:
                return event
            case WSMessageType.REQUEST_MATCHING:
                return self._handle_request_matching(db, event)
            
    def _handle_request_matching(self, db: Session, event: dict):
        matching_request: MatchingRequest = self.repo.create_matching_request(db, event["user_id"], event["room_id"])
        if matching_request is None:
            raise Exception("매칭 요청 생성 실패")
        
        event["matching_request_id"] = matching_request.id
        event["to_user_id"] = matching_request.to_user_id
        return event
    
    def getChatRooms(self, db: Session, user_id: UUID) -> list[ChatRoomInfo]:
        chatrooms = self.repo.get_my_chatrooms(db, user_id)
        return [ChatRoomInfo(
            room_id=room.id, # type: ignore
            opponent_name=room.opponent_name,
            last_message=room.last_message,
            updated_at=room.updated_at.isoformat()
        ) for room in chatrooms]

    def create_chat_room(self, db: Session, announcement_id: UUID, user_id: UUID, name: str):
        return self.repo.create_chatroom(db, announcement_id, user_id, name)
    
    def get_chat_logs(self, db: Session, room_id: UUID, last_message_id: UUID | None = None, limit: int = 50):
        logs =  self.repo.get_chat_logs(db, room_id, last_message_id, limit)
        res = []
        for log, sender_name in logs:
            log.sender_name = sender_name
            res.append(
                ChatLogResponse(
                    sender_name=sender_name,
                    content=log.content,
                    timestamp=log.timestamp.isoformat(),
                    read=log.read
                )
            )
        return res

    def create_chat_log(self, db: Session, room_id: UUID, author_id: UUID, content: str):
        return self.repo.create_chat_log(db, room_id, author_id, content)
