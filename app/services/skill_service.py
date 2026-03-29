from app.repositories.skill_repository import SkillRepository


class SkillService:
    def __init__(self, repo: SkillRepository):
        self.repo = repo
