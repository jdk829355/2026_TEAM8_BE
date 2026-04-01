from pydantic import BaseModel
from typing import List


# Request Models
class WantToLearnRequest(BaseModel):
    want_to_skill: List[str]


class CanToTeachRequest(BaseModel):
    can_teach_skill: List[str]


# Response Models
class ViewAllSkillsResponse(BaseModel):
    can_teach_skill: List[str]
    want_to_skill: List[str]


class ViewWantToLearnResponse(BaseModel):
    want_to_skill: List[str]


class ViewCanToTeachResponse(BaseModel):
    can_teach_skill: List[str]


class EditWantToLearnRequest(BaseModel):
    want_to_skill: List[str]


class EditCanToTeachRequest(BaseModel):
    can_teach_skill: List[str]
