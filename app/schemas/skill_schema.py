from pydantic import BaseModel
from typing import List


class SkillItem(BaseModel):
    name: str
    category: str


# Request Models
class WantToLearnRequest(BaseModel):
    want_to_skill: List[SkillItem]


class CanToTeachRequest(BaseModel):
    can_teach_skill: List[SkillItem]


# Response Models
class ViewAllSkillsResponse(BaseModel):
    can_teach_skill: List[SkillItem]
    want_to_skill: List[SkillItem]


class ViewWantToLearnResponse(BaseModel):
    want_to_skill: List[SkillItem]


class ViewCanToTeachResponse(BaseModel):
    can_teach_skill: List[SkillItem]


class EditWantToLearnRequest(BaseModel):
    want_to_skill: List[SkillItem]


class EditCanToTeachRequest(BaseModel):
    can_teach_skill: List[SkillItem]


class CreateSkillRequest(BaseModel):
    name: str
    category: str


class SkillItemResponse(BaseModel):
    name: str
    category: str
