from app.repositories.matching_repository import MatchingRepository


class MatchingService:
    def __init__(self, repo: MatchingRepository):
        self.repo = repo
