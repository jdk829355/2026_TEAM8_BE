import json
import aioredis
import os

class EventPublisher:
    def __init__(self, redis):
        self.redis = redis

    async def publish(self, channel: str, event: dict):
        await self.redis.publish(channel, json.dumps(event))

# 전역 객체
redis_url = os.getenv("REDIS_URL", "redis://localhost")
redis = aioredis.from_url(redis_url)

publisher = EventPublisher(redis)