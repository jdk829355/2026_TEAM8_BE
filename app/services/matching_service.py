from app.repositories.matching_repository import MatchingRepository
from app.schemas.chat_schema import WSMessageType


class MatchingService:
    def __init__(self, repo: MatchingRepository):
        self.repo: MatchingRepository = repo

    def accept_matching_request(self, db, matching_request_id):
        result = self.repo.create_matching_from_request(db, matching_request_id)
        if result is None:
            raise ValueError("matching request not found")
        matching_id, host_user_id, guest_user_id = result
        return {
            "type": WSMessageType.REPLY_MATCHING,
            "user_id": host_user_id,
            "to_user_id": guest_user_id,
            "matching_id": matching_id,
        }

    def reject_matching_request(self, db, matching_request_id):
        return self.repo.reject_matching_request(db, matching_request_id)
