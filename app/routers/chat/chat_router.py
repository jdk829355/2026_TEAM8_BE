import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.dependencies import get_chat_service
from app.core.verify_jwt import get_current_user_id, get_current_user_id_ws
from app.dependencies.database import get_db
from app.schemas.chat_schema import (
    ChatLogResponse,
    ChatRoomInfo,
    CreateRoomRequest,
    CreateRoomResponse,
)
from app.realtime.connection_manager import manager
from app.realtime.event_handler import handler
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/rooms", response_model=list[ChatRoomInfo])
def get_chat_rooms(
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
    service: ChatService = Depends(get_chat_service),
) -> list[ChatRoomInfo]:
    return service.getChatRooms(db=db, user_id=user_id)


@router.post("/room", response_model=CreateRoomResponse)
def create_chat_room(
    create_room_request: CreateRoomRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: ChatService = Depends(get_chat_service),
    db: Session = Depends(get_db),
):
    room = service.create_chat_room(
        db=db,
        announcement_id=create_room_request.announcement_id,
        user_id=user_id,
        name=create_room_request.name,
    )
    return CreateRoomResponse(room_id=room.id)  # type: ignore


@router.websocket("/")
async def chat_websocket(
    ws: WebSocket,
    user_id: str = Depends(get_current_user_id_ws),
    service: ChatService = Depends(get_chat_service),
    db: Session = Depends(get_db),
):
    logger = logging.getLogger(__name__)
    token_user_id = UUID(user_id)

    await manager.connect(ws)
    try:
        while True:
            try:
                data = await ws.receive_text()
                event = json.loads(data)
                logger.info(f"Received event: {event}")
                service.handle_ws_message(db=db, event=event)
                await handler.handle(event, ws, token_user_id)
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected by client")
                break
            except (json.JSONDecodeError, ValidationError, ValueError, KeyError) as e:
                logger.error(f"WebSocket event validation error: {e}")
                await ws.send_json({"error": "invalid websocket event"})
                continue
            except Exception as e:
                if str(e) == "이미 매칭이 존재하는 채팅방입니다.":
                    logger.warning(f"Matching already exists for room: {e}")
                    await ws.send_json({"error": "matching already exists for this room"})
                    continue
                logger.exception(f"WebSocket event handling error: {e}")
                await ws.send_json({"error": "internal websocket error"})
                continue
    finally:
        manager.disconnect(ws)


@router.get("/room/{room_id}", response_model=list[ChatLogResponse])
def get_chat_room(
    room_id: str,
    last_message_id: str | None = None,
    service: ChatService = Depends(get_chat_service),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    _ = user_id
    return service.get_chat_logs(
        db=db,
        room_id=UUID(room_id),
        last_message_id=(UUID(last_message_id) if last_message_id else None),
    )


@router.post("/room/{room_id}/ai-evaluate")
def evaluate_chat_room_ai(room_id: str):
    _ = room_id
    return {"message": "evaluate_chat_room_ai handler"}


