from pydantic import BaseModel
from typing import List

# Response Models
class MatchingItem(BaseModel):
    name: str
    teaching_skill: str
    learning_skill: str
    status: str

class ViewMyMatchingListResponse(BaseModel):
    items: List[MatchingItem]

class ViewDetailMatchingResponse(BaseModel):
    opponent_name: str
    teaching_skill: str
    learning_skill: str
    message: str

class AcceptMatchingRequest(BaseModel):
    accept: bool