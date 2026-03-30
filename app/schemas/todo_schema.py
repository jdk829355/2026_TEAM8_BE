from pydantic import BaseModel
from typing import List

# Request Models
class CreateToDoCandidateRequest(BaseModel):
    room_id: str

class CreateToDoRequest(BaseModel):
    matching_id: str
    skill_id: str
    task: str

class UpdateToDoRequest(BaseModel):
    task: str
    is_completed: bool

# Response Models
class ToDoItem(BaseModel):
    todo_id: int
    task: str
    is_completed: bool

class ViewMyToDoResponse(BaseModel):
    items: List[ToDoItem]

class ViewOpponentToDoResponse(BaseModel):
    items: List[ToDoItem]

class UpdateToDoResponse(BaseModel):
    todo_id: int
    task: str
    is_completed: bool

class ToDoCandidate(BaseModel):
    id: str
    name: str
    skill: str

class ViewToDoCandidateResponse(BaseModel):
    candidates: List[ToDoCandidate]

class CreateToDoCandidateResponse(BaseModel):
    candidates: List[ToDoCandidate]
