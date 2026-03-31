import json
import os
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis

class EventPublisher:
    def __init__(self, redis):
        self.redis = redis

    async def publish(self, channel: str, event: dict):
        payload = jsonable_encoder(event)
        await self.redis.publish(channel, json.dumps(payload))

# 전역 객체
redis_url = os.getenv("REDIS_URL", "redis://localhost")
redis = Redis.from_url(redis_url)

publisher = EventPublisher(redis)