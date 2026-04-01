from pydantic import BaseModel


# Request Models
class CreateAnnounceRequest(BaseModel):
    want_to_skill: str
    can_teach_skill: str
    want_to_message: str
    can_teach_message: str
    can_teach_difficulty: str
    want_to_difficulty: str


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
    user_id: str
    want_to_skill: str
    can_teach_skill: str


class ViewDetailAnnounceResponse(BaseModel):
    id: str
    user_id: str
    username: str
    want_to_skill: str
    can_teach_skill: str
    want_to_message: str
    can_teach_message: str
    can_teach_difficulty: str
    want_to_difficulty: str


class EditAnnounceResponse(BaseModel):
    id: str
    user_id: str
    want_to_skill: str
    can_teach_skill: str
    want_to_message: str
    can_teach_message: str
    can_teach_difficulty: str
    want_to_difficulty: str
