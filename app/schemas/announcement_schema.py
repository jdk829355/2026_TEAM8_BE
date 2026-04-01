from pydantic import BaseModel

# Request Models
class CreateAnnounceRequest(BaseModel):
    wantToSkill: str
    canTeachSkill: str
    wantToMessage: str
    canTeachMessage: str
    canTeachDifficulty: str
    wantToDifficulty: str


class EditAnnounceRequest(BaseModel):
    want_to_skill: str | None = None
    can_teach_skill: str | None = None
    want_to_message: str | None = None
    can_teach_message: str | None = None
    can_teach_difficulty: str | None = None
    want_to_difficulty: str | None = None


# Response Models
class AnnounceItem(BaseModel):
    id: str
    username: str
    userId: str
    wantToSkill: str
    canTeachSkill: str


class ViewDetailAnnounceResponse(BaseModel):
    id: str
    userId: str
    username: str
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
