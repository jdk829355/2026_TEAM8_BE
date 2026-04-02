from functools import lru_cache
import os
from typing import List
from uuid import UUID

from huggingface_hub import InferenceClient

from app.schemas.todo_schema import ToDoItem

class AiService:
    def __init__(self, chat_repository, todo_repository):
        self.chat_repository = chat_repository
        self.todo_repository = todo_repository
        self._client: InferenceClient = InferenceClient(
                    provider="hf-inference",
                    api_key=os.environ["HF_TOKEN"],
            )
        self._model = os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    @lru_cache(maxsize=128)
    def encode_skill_name(self, skill_name: str) -> list[float]:
        embedding = self._client.feature_extraction(text=skill_name, model = self._model)
        return embedding.tolist()
    
    def create_todo_by_ai(self, room_id: UUID) -> List[ToDoItem]:
        return []