from pydantic import BaseModel
from typing import List

# Response Models
class MatchingItem(BaseModel):
    name: str
    teaching_skill: str
    learning_skill: str
    status: str

class ViewMyMatchingListResponse(BaseModel):
    items: List[MatchingItem]

class ViewDetailMatchingResponse(BaseModel):
    opponent_name: str
    teaching_skill: str
    learning_skill: str
    message: str

class AcceptMatchingRequest(BaseModel):
    accept: bool


class SentMatchingRequest(BaseModel):
    """보낸 매칭 요청 아이템"""
    matching_request_id: str
    opponent_name: str
    room_id: str

class ReceivedMatchingRequest(BaseModel):
    """받은 매칭 요청 아이템"""
    matching_request_id: str
    opponent_name: str
    room_id: str

class MatchingRequestsResponse(BaseModel):
    """/matching/requests 응답 전체 모델"""
    send: List[SentMatchingRequest]
    receive: List[ReceivedMatchingRequest]