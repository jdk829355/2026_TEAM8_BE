from app.models import MatchingRequest
from app.repositories.announcement_repository import AnnouncementRepository
from app.repositories.matching_repository import MatchingRepository
from app.schemas.chat_schema import WSMessageType
from app.schemas.matching_schema import MatchingRequestsResponse, SentMatchingRequest, ReceivedMatchingRequest


class MatchingService:
    def __init__(self, repo: MatchingRepository, announcement_repo: AnnouncementRepository):
        self.repo: MatchingRepository = repo
        self.announcement_repo: AnnouncementRepository = announcement_repo

    def accept_matching_request(self, db, matching_request_id):
        result = self.repo.create_matching_from_request(db, matching_request_id)
        if result is None:
            raise ValueError("matching request not found")
        matching_id, host_user_id, guest_user_id, announcement_id = result
        announcement = self.announcement_repo.get_by_id(db, announcement_id)
        if announcement is None:
            raise ValueError("announcement not found")
        self.announcement_repo.update(db, announcement, {"visible": False})
        return {
            "type": WSMessageType.REPLY_MATCHING,
            "user_id": host_user_id,
            "to_user_id": guest_user_id,
            "matching_id": matching_id,
            "accept": True,
        }

    def reject_matching_request(self, db, matching_request_id):
        res = self.repo.matching_request_info(db, matching_request_id)
        if res is None:
            return (False, None)

        host_id = res["host_user_id"]
        guest_id = res["guest_user_id"]
        is_deleted = self.repo.reject_matching_request(db, matching_request_id)
        if not is_deleted:
            return (False, None)

        return (is_deleted, {
            "type": WSMessageType.REPLY_MATCHING,
            "user_id": guest_id,
            "to_user_id": host_id,
            "accept": False,
        })

    def get_matching_request(self, db, user_id):
        matching_request_send, matching_request_receive = self.repo.get_matching_request(db, user_id)
        return MatchingRequestsResponse(
            send=[SentMatchingRequest(
                matching_request_id = str(matching_request[0].id),
                opponent_name=matching_request[1],
                room_id=str(matching_request[0].room_id),
            ) for matching_request in matching_request_send],
            receive=[ReceivedMatchingRequest(
                matching_request_id=str(matching_request[0].id),
                opponent_name=matching_request[1],
                room_id=str(matching_request[0].room_id),
            ) for matching_request in matching_request_receive],
        )
