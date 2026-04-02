from functools import lru_cache
import os
from typing import List
from uuid import UUID

from huggingface_hub import InferenceClient
from sqlalchemy.orm import Session

from app.models.chat_models import ChatLog, Chatroom, JoinChat
from app.models.skill_models import Skill
from app.repositories.chat_repository import ChatRepository
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo_schema import GeneratedTodoItem, ToDoItem
from app.dependencies.ai.todo_generator import run as generate_todo_by_ai

class AiService:
    def __init__(self, chat_repository: ChatRepository, todo_repository: TodoRepository):
        self.chat_repository: ChatRepository = chat_repository
        self.todo_repository: TodoRepository = todo_repository
        self._client: InferenceClient = InferenceClient(
                    provider="hf-inference",
                    api_key=os.environ["HF_TOKEN"],
            )
        self._model = os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    @lru_cache(maxsize=128)
    def encode_skill_name(self, skill_name: str) -> list[float]:
        embedding = self._client.feature_extraction(text=skill_name, model = self._model)
        return embedding.tolist()
    
    def _build_conversation(self, chat_logs: list[ChatLog], chatroom: Chatroom, participants: list) -> dict:
        messages = [
            {
                "sender": str(log.author_id),
                "text": log.content
            } for log in chat_logs
        ]

        return {
            "participants": participants,
            "messages": messages,
        }
    
    def _build_users(self, skills: list[Skill], participants: list) -> dict:
        skill_names = [skill.name for skill in skills]
        user_ids = [str(p) for p in participants]
        users = {
            user_id: {
                "teach_subjects": skill_names,
                "learn_subjects": skill_names,
                "level": "medium"
            } for user_id in user_ids
        }
        return users

    
    def create_todo_by_ai(self, db: Session, room_id: UUID) -> List[GeneratedTodoItem]:
        conversation = [log[0] for log in self.chat_repository.get_chat_logs(db, room_id)]
        chatroom = db.query(Chatroom).filter(Chatroom.id == room_id).first()
        participants = [user[0] for user in db.query(JoinChat.user_id).filter(JoinChat.room_id == room_id).all()]
        skills: list[Skill] = self.todo_repository.get_skills_by_announcement(db, chatroom.announcement_id) # type: ignore

        todos = generate_todo_by_ai(
            conversation=self._build_conversation(conversation, chatroom, participants),
            users=self._build_users(skills, participants)
        )

        todos = [
            GeneratedTodoItem(
                name=todo["task_name"],
                skill=todo["subject"]
            ) for todo in todos
        ]
        return todos