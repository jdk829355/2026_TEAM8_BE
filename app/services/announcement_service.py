from app.repositories.announcement_repository import AnnouncementRepository


class AnnouncementService:
    def __init__(self, repo: AnnouncementRepository):
        self.repo = repo
