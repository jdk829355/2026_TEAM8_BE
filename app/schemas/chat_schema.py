from enum import Enum

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


# Response Models
class ChatRoomInfo(BaseModel):
    room_id: UUID
    opponent_name: str
    last_message: str
    updated_at: str

class ChatLogResponse(BaseModel):
    sender_name: str
    content: str
    timestamp: str
    read: bool

class CreateRoomRequest(BaseModel):
    announcement_id: UUID
    name: str

class CreateRoomResponse(BaseModel):
    room_id: UUID


class WSMessageType(str, Enum):
    JOIN_CHAT = "JOIN_CHAT"
    LEAVE_CHAT = "LEAVE_CHAT"
    REQUEST_MATCHING = "REQUEST_MATCHING"
    REPLY_MATCHING = "REPLY_MATCHING"
    SEND_MESSAGE = "SEND_MESSAGE"
    RECV_MESSAGE = "RECV_MESSAGE"
    RECEIVE_MATCHING = "RECEIVE_MATCHING"

class WSSubscribeMessage(BaseModel):
    type: WSMessageType
    user_id: UUID
    room_id: Optional[UUID] = None

class WSSendMessage(BaseModel):
    type: WSMessageType
    user_id: UUID
    room_id: UUID
    content: str

class WSRequestMatchingMessage(BaseModel):
    type: WSMessageType
    user_id: UUID
    to_user_id: UUID|None = None
    room_id: UUID
    matching_request_id: UUID|None = None

class WSReplyMatchingMessage(BaseModel):
    type: WSMessageType
    user_id: UUID
    to_user_id: UUID | None = None
    matching_request_id: UUID
    room_id: UUID
    accept: bool