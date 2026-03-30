import json

from app.realtime.channels import chat_room, user_event
from app.realtime.connection_manager import ConnectionManager
from app.schemas.chat_schema import WSMessageType


class EventSubscriber:
    def __init__(self, redis, manager):
        self.redis = redis
        self.manager: ConnectionManager = manager

    async def _handle_send_message(self, event):
        await self.manager.send_to_channel(chat_room(event["room_id"]), event)

    async def _handle_request_matching(self, event):
        await self.manager.send_to_channel(user_event(event["user_id"]), event)
        event["type"] = WSMessageType.RECEIVE_MATCHING
        await self.manager.send_to_channel(user_event(event["to_user_id"]), event)

    async def _handle_reply_matching(self, event):
        await self.manager.send_to_channel(user_event(event["user_id"]), event)
        await self.manager.send_to_channel(user_event(event["to_user_id"]), event)

    async def start(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(chat_room("*"), user_event("*"))

        async for message in pubsub.listen():
            match message["type"]:
                case WSMessageType.SEND_MESSAGE:
                    event = json.loads(message)
                    event["type"] = WSMessageType.RECV_MESSAGE
                    await self._handle_send_message(event)
                case WSMessageType.REQUEST_MATCHING:
                    event = json.loads(message)
                    await self._handle_request_matching(event)
                case WSMessageType.REPLY_MATCHING:
                    event = json.loads(message)
                    await self._handle_reply_matching(event)