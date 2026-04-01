from pydantic import BaseModel
from typing import List, Optional


# Request Models
class EditMyProfileRequest(BaseModel):
    name: str
    description: str


# Response Models
class SearchUserProfileResponse(BaseModel):
    name: str
    email: str
    can_teach_skills: List[str]
    want_to_skills: List[str]
