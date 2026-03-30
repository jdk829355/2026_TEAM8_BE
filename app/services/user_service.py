from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def update_user_info(self, db, user_id, payload):
        payload = {
            "description": payload.get("description"),
            "passion": payload.get("passion"),
            "speech": payload.get("speech"),
            "purpose": payload.get("purpose"),
        }
        return self.repo.update_user(db, user_id, payload)