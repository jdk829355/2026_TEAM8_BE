from pydantic import BaseModel

class ViewAnnounce(BaseModel):
    [
     {
        "id": str,
        "username": str,
        "user_id": str,
        "want_to_skill": str,
        "can_teach_skill": str
    }
    ]
    
class ViewDetailAnnounce(BaseModel):
    {
  "id": "str",
  "userId": "str",
  "wantToSkill": "str",
  "canTeachSkill": "str",
  "wantToMessage": "str",
  "canTeachMessage": "str",
  "canTeachDifficulty": "str",
  "wantToDifficulty": "str"
}
    
class CreateAnnounce(BaseModel):
    {
  "wantToSkill": "uuid.UUID",
  "canTeachSkill": "uuid.UUID",
  "wantToMessage": "str",
  "canTeachMessage": "str",
  "canTeachDifficulty": "str",
  "wantToDifficulty": "str"
}
    
class EditAnnounceRequest(BaseModel):
    {
  "wantToSkill": "uuid.UUID",
  "canTeachSkill": "uuid.UUID",
  "wantToMessage": "str",
  "canTeachMessage": "str",
  "canTeachDifficulty": "str",
  "wantToDifficulty": "str"
}
    
class EditAnnounceResponse(BaseModel):
    {
  "id": "str",
  "userId": "str",
  "wantToSkill": "str",
  "canTeachSkill": "str",
  "wantToMessage": "str",
  "canTeachMessage": "str",
  "canTeachDifficulty": "str",
  "wantToDifficulty": "str"
}