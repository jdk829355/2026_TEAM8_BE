from fastapi import APIRouter

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)


@router.post("")
def create_todo():
    return {"message": "create_todo handler"}


@router.get("/my-tasks")
def get_my_tasks():
    return {"message": "get_my_tasks handler"}


@router.get("/{matching_id}/opponent-tasks")
def get_opponent_tasks(matching_id: str):
    _ = matching_id
    return {"message": "get_opponent_tasks handler"}


@router.patch("/{todo_id}")
def update_todo(todo_id: str):
    _ = todo_id
    return {"message": "update_todo handler"}


@router.get("/{matching_id}/status")
def get_todo_status(matching_id: str):
    _ = matching_id
    return {"message": "get_todo_status handler"}


@router.post("/generated_todo")
def create_generated_todo():
    return {"message": "create_generated_todo handler"}


@router.get("/generated_todo")
def get_generated_todo():
    return {"message": "get_generated_todo handler"}
