from app.repositories.todo_repository import TodoRepository


class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo
