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
    teaching_skills: List[str]
    learning_skills: List[str]
