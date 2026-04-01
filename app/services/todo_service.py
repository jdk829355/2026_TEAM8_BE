from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.todo_repository import TodoRepository

class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo

    # [내 투두 조회]
    def get_my_tasks(self, db: Session, user_id: UUID):
        return self.repo.get_todos_by_user(db, user_id)

    # [상대방 투두 조회] 
    # matching_id와 상대방 user_id(opponent_id)가 필요합니다.
    def get_opponent_tasks(self, db: Session, matching_id: UUID, opponent_id: UUID):
        return self.repo.get_todos_by_matching_user(db, matching_id, opponent_id)

    # [투두 완료 상태 업데이트]
    def update_todo_status(self, db: Session, user_id: UUID, task_id: UUID, is_completed: bool):
        return self.repo.update_todo_status(db, user_id, task_id, is_completed)

    # [후보군 채택 시 - Task 생성]
    def create_todo_from_candidate(self, db: Session, user_id: UUID, matching_id: UUID, skill_id: UUID, task_name: str):
        # Task 생성 (user_id 포함)
        return self.repo.create_task(db, user_id=user_id, name=task_name, skill_id=skill_id, matching_id=matching_id)

    # [후보군 조회]
    def get_candidates(self, db: Session, chatroom_id: UUID):
        return self.repo.get_generated_todos_by_chatroom(db, chatroom_id)