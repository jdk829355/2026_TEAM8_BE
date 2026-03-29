from pydantic import BaseModel

class CreateToDo(BaseModel):
    {
    "matching_id": str,
    "skill_id": str,
    "task": str
    }
    
class ViewMyToDo(BaseModel):
    [
     {
           "todo_id": int, 
           "task": str, 
           "is_completed": bool
      }
]
class ViewOpponentToDo(BaseModel):
    [
     {
           "todo_id": int, 
           "task": str, 
           "is_completed": bool
      }
]

class UpdateToDoRequest(BaseModel):
    {
  "task": "str",
  "is_completed": "bool"
}

class UpdateToDoResponse(BaseModel):
    {
  "todo_id": int,
  "task": "str",
  "is_completed": "bool"
}

class CreateToDoCandidateRequest(BaseModel):
    {
    "room_id": str
}

class CreateToDoCandidateResponse(BaseModel):
    {
    "id": int, 
    "name": str, 
    }
    
class ViewToDoCandidate(BaseModel):
    [
     {
           "id": int, 
           "name": str, 
      }
]

class SelcetToDoCandidateRequest(BaseModel):
    {
    "id": int
}

