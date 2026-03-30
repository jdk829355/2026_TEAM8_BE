import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session

from app.core.dependencies import get_chat_service
from app.core.verify_jwt import get_current_user_id, get_current_user_id_ws
from app.dependencies.database import get_db
from app.schemas.chat_schema import ChatLogResponse, ChatRoomInfo, CreateRoomRequest, CreateRoomResponse, WSMessageType
from app.realtime.connection_manager import manager
from app.realtime.event_handler import handler
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/rooms", response_model= list[ChatRoomInfo])
def get_chat_rooms(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id), service: ChatService = Depends(get_chat_service)) -> list[ChatRoomInfo]:
    return service.getChatRooms(db=db, user_id=UUID(user_id))
    


@router.post("/room", response_model= CreateRoomResponse)
def create_chat_room(create_room_request: CreateRoomRequest, user_id: str = Depends(get_current_user_id), service: ChatService = Depends(get_chat_service), db: Session = Depends(get_db)):
    room = service.create_chat_room(db=db, announcement_id=create_room_request.announcement_id, user_id=UUID(user_id), name=create_room_request.name)
    return CreateRoomResponse(room_id=room.id) # type: ignore


@router.websocket("/")
async def chat_websocket(ws: WebSocket, user_id: str = Depends(get_current_user_id_ws)):
    logger = logging.getLogger("__name__")
    

    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            event = json.loads(data)
            logger.info(f"Received event: {event}")
            await handler.handle(event, ws)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(ws)


@router.get("/room/{room_id}", response_model= list[ChatLogResponse])
def get_chat_room(room_id: str, last_message_id: str|None = None, service: ChatService = Depends(get_chat_service), db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id) ):
    return service.get_chat_logs(db=db, room_id=UUID(room_id), last_message_id=(UUID(last_message_id) if last_message_id else None))


@router.post("/room/{room_id}/ai-evaluate")
def evaluate_chat_room_ai(room_id: str):
    _ = room_id
    return {"message": "evaluate_chat_room_ai handler"}


