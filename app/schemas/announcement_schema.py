from pydantic import BaseModel
from typing import List
from uuid import UUID

# Request Models
class CreateAnnounceRequest(BaseModel):
    wantToSkill: str
    canTeachSkill: str
    wantToMessage: str
    canTeachMessage: str
    canTeachDifficulty: str
    wantToDifficulty: str

class EditAnnounceRequest(BaseModel):
    wantToSkill: UUID
    canTeachSkill: UUID
    wantToMessage: str
    canTeachMessage: str
    canTeachDifficulty: str
    wantToDifficulty: str

# Response Models
class AnnounceItem(BaseModel):
    id: str
    username: str
    user_id: str
    want_to_skill: str
    can_teach_skill: str

class ViewAnnounceResponse(BaseModel):
    announcements: List[AnnounceItem]

class ViewDetailAnnounceResponse(BaseModel):
    id: str
    userId: str
    wantToSkill: str
    canTeachSkill: str
    wantToMessage: str
    canTeachMessage: str
    canTeachDifficulty: str
    wantToDifficulty: str

class EditAnnounceResponse(BaseModel):
    id: str
    userId: str
    wantToSkill: str
    canTeachSkill: str
    wantToMessage: str
    canTeachMessage: str
    canTeachDifficulty: str
    wantToDifficulty: str
