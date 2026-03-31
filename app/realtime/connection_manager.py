from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.connections = {}  # ws -> set(channels)
        self.channel_subscribers = defaultdict(set)  # channel -> set(ws)

    async def connect(self, ws):
        await ws.accept()
        self.connections[ws] = set()

    def disconnect(self, ws):
        channels = self.connections.get(ws, set())

        for ch in channels:
            self.channel_subscribers[ch].discard(ws)

        self.connections.pop(ws, None)

    def subscribe(self, ws, channel: str):
        self.connections[ws].add(channel)
        self.channel_subscribers[channel].add(ws)

    def unsubscribe(self, ws, channel: str):
        self.connections[ws].discard(channel)
        self.channel_subscribers[channel].discard(ws)

    async def send_to_channel(self, channel: str, message: dict):
        for ws in self.channel_subscribers[channel]:
            await ws.send_json(message)


# 전역 객체
manager = ConnectionManager()