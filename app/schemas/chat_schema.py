from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

# Request Models
class EnterChatRoomRequest(BaseModel):
    announcement_id: UUID

# Response Models
class ChatRoomInfo(BaseModel):
    room_id: UUID
    opponent_name: str
    last_message: str
    updated_at: str

class SearchChatListResponse(BaseModel):
    rooms: List[ChatRoomInfo]

class EnterChatRoomResponse(BaseModel):
    room_id: UUID
