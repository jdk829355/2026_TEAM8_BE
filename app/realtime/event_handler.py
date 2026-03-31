from uuid import UUID

from fastapi import WebSocket

from app.realtime.publisher import EventPublisher
from app.schemas.chat_schema import (
    WSMessageType,
    WSRequestMatchingMessage,
    WSSendMessage,
    WSSubscribeMessage,
)
from app.realtime.connection_manager import manager
from app.realtime.channels import user_event, chat_room
from app.realtime.publisher import publisher


class EventHandler:
    def __init__(self, publisher):
        self.publisher: EventPublisher = publisher

    async def handle(self, event: dict, ws: WebSocket, token_user_id: UUID):
        try:
            message_type = event["type"]
        except KeyError as exc:
            raise ValueError("event type is required") from exc

        match event["type"]:
            case WSMessageType.JOIN_CHAT:
                validated_event = WSSubscribeMessage.model_validate(event)
                self._validate_user(validated_event.user_id, token_user_id)
                self._handle_join_chat(validated_event, ws)
            case WSMessageType.SEND_MESSAGE:
                validated_event = WSSendMessage.model_validate(event)
                self._validate_user(validated_event.user_id, token_user_id)
                await self._handle_send_message(validated_event)
            case WSMessageType.REQUEST_MATCHING:
                validated_event = WSRequestMatchingMessage.model_validate(event)
                self._validate_user(validated_event.user_id, token_user_id)
                await self._handle_request_matching(validated_event)
            case _:
                raise ValueError(f"unsupported event type: {message_type}")

    @staticmethod
    def _validate_user(event_user_id: UUID, token_user_id: UUID) -> None:
        if event_user_id != token_user_id:
            raise ValueError("event user_id does not match token user_id")

    def _handle_join_chat(self, event: WSSubscribeMessage, ws: WebSocket):
        manager.subscribe(ws, user_event(str(event.user_id)))
        if event.room_id is not None:
            manager.subscribe(ws, chat_room(str(event.room_id)))

    async def _handle_send_message(self, event: WSSendMessage):
        await self.publisher.publish(
            chat_room(str(event.room_id)),
            event.model_dump(mode="json"),
        )

    async def _handle_request_matching(self, event: WSRequestMatchingMessage):
        await self.publisher.publish(
            user_event(str(event.user_id)),
            event.model_dump(mode="json"),
        )


handler = EventHandler(publisher)
