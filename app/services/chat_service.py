from app.repositories.chat_repository import ChatRepository


class ChatService:
    def __init__(self, repo: ChatRepository):
        self.repo = repo
