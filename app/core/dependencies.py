from functools import lru_cache

from fastapi import Depends

from app.repositories.announcement_repository import AnnouncementRepository
from app.repositories.auth_repository import AuthRepository
from app.repositories.chat_repository import ChatRepository
from app.repositories.matching_repository import MatchingRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.todo_repository import TodoRepository
from app.repositories.user_repository import UserRepository
from app.services.ai_service import AiService
from app.services.announcement_service import AnnouncementService
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.services.matching_service import MatchingService
from app.services.skill_service import SkillService
from app.services.todo_service import TodoService
from app.services.user_service import UserService

@lru_cache()
def get_ai_service() -> AiService:
    return AiService()

@lru_cache()
def get_auth_repository() -> AuthRepository:
    return AuthRepository()


@lru_cache()
def get_skill_repository(ai_service: AiService = Depends(get_ai_service)) -> SkillRepository:
    return SkillRepository(ai_service)


@lru_cache()
def get_matching_repository() -> MatchingRepository:
    return MatchingRepository()


@lru_cache()
def get_chat_repository() -> ChatRepository:
    return ChatRepository()


@lru_cache()
def get_todo_repository() -> TodoRepository:
    return TodoRepository()


@lru_cache()
def get_user_repository() -> UserRepository:
    return UserRepository()


@lru_cache()
def get_announcement_repository() -> AnnouncementRepository:
    return AnnouncementRepository()



@lru_cache()
def get_auth_service(
    repo: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(repo)


@lru_cache()
def get_skill_service(
    repo: SkillRepository = Depends(get_skill_repository),
    ai_service: AiService = Depends(get_ai_service),
) -> SkillService:
    return SkillService(repo, ai_service)


@lru_cache()
def get_matching_service(
    repo: MatchingRepository = Depends(get_matching_repository),
    announcement_repo: AnnouncementRepository = Depends(get_announcement_repository),
) -> MatchingService:
    return MatchingService(repo, announcement_repo)


@lru_cache()
def get_chat_service(
    repo: ChatRepository = Depends(get_chat_repository),
) -> ChatService:
    return ChatService(repo)



@lru_cache()
def get_todo_service(
    repo: TodoRepository = Depends(get_todo_repository),
) -> TodoService:
    return TodoService(repo)


@lru_cache()
def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


@lru_cache()
def get_announcement_service(
    repo: AnnouncementRepository = Depends(get_announcement_repository),
) -> AnnouncementService:
    return AnnouncementService(repo)
