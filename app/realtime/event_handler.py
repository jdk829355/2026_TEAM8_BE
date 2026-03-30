from fastapi import WebSocket

from app.realtime.publisher import EventPublisher
from app.schemas.chat_schema import WSMessageType
from app.realtime.connection_manager import manager
from app.realtime.channels import user_event, chat_room
from app.realtime.publisher import publisher


class EventHandler:
    def __init__(self, publisher):
        self.publisher: EventPublisher = publisher

    async def handle(self, event, ws:WebSocket):
        match event["type"]:
            case WSMessageType.JOIN_CHAT:
                self._handle_join_chat(event, ws)
            case WSMessageType.SEND_MESSAGE:
                await self._handle_send_message(event)
            case WSMessageType.REQUEST_MATCHING:
                await self._handle_request_matching(event)

    def _handle_join_chat(self, event, ws:WebSocket):
        manager.subscribe(ws, user_event(event["user_id"]))
        manager.subscribe(ws, chat_room(event["room_id"]))
    
    async def _handle_send_message(self, event):
        await self.publisher.publish(chat_room(event["room_id"]), event)

    async def _handle_request_matching(self, event):
        await self.publisher.publish(user_event(event["user_id"]), event)

handler = EventHandler(publisher)