from pydantic import BaseModel
from typing import List

# Request Models
class WantToLearnRequest(BaseModel):
    learning_skill: List[str]

class CanToTeachRequest(BaseModel):
    teaching_skill: List[str]

# Response Models
class ViewAllSkillsResponse(BaseModel):
    teaching_skill: List[str]
    learning_skill: List[str]

class ViewWantToLearnResponse(BaseModel):
    learning_skill: List[str]

class ViewCanToTeachResponse(BaseModel):
    teaching_skill: List[str]

class EditWantToLearnRequest(BaseModel):
    learning_skill: List[str]

class EditCanToTeachRequest(BaseModel):
    teaching_skill: List[str]
