from fastapi import Depends

from app.core.dependencies import get_chat_service
from app.realtime.publisher import publisher
from app.repositories.chat_repository import ChatRepository
from app.repositories.matching_repository import MatchingRepository
from app.schemas.chat_schema import WSMessageType


class MatchingService:
    def __init__(self, repo: MatchingRepository, chat_repo: ChatRepository):
        self.repo: MatchingRepository = repo
        self.chat_repo: ChatRepository = chat_repo

    def accept_matching_request(self, db, matching_request_id,):
        res = self.chat_repo.matching_request_to_announcement(db, matching_request_id)
        if res is None:
            raise Exception("매칭 요청 처리 실패")
        announcement_id, host_user_id, guest_user_id = res
        matching = self.repo.create_matching(db, announcement_id, host_user_id, guest_user_id)
        if matching is None:
            raise Exception("매칭 생성 실패")
        
        chatroom = self.chat_repo.get_my_chatrooms(db, host_user_id)
        if chatroom is None:
            raise Exception("채팅방 조회 실패")
        
        target_room = None
        for room in chatroom:
            if room.announcement_id == announcement_id: # type: ignore
                target_room = room
                break

        target_room.matching_id = matching.id # type: ignore
        db.commit()

        self.repo.accept_matching_request(db, matching_request_id, matching.id) # type: ignore
        return {
            "type": WSMessageType.REPLY_MATCHING,
            "user_id": host_user_id,
            "to_user_id": guest_user_id,
            "matching_id": matching.id,
        }
    
    def reject_matching_request(self, db, matching_request_id,):
        return self.repo.reject_matching_request(db, matching_request_id)