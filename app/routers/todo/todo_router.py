from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.dependencies.database import get_db
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from app.schemas.todo_schema import (
    CreateToDoRequest, 
    UpdateToDoRequest, 
    ViewMyToDoResponse, 
    ToDoItem,
    ViewToDoCandidateResponse,
    CreateToDoCandidateRequest,
    ToDoCandidate
)

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

# [의존성 주입] Service 객체를 생성하여 주입해주는 함수
def get_todo_service():
    return TodoService(TodoRepository())

# 테스트용 고정 UUID (나중에 로그인 기능 완성 시 삭제)
TEST_USER_ID = UUID("123e4567-e89b-12d3-a456-426614174000")

# ---------------------------------------------------------
# 1. 일반 Todo 관리 (조회, 생성, 업데이트)
# ---------------------------------------------------------

@router.get("/my-tasks", response_model=ViewMyToDoResponse)
def get_my_tasks(
    db: Session = Depends(get_db),
    service: TodoService = Depends(get_todo_service)
):
    """
    용도: 현재 로그인한 유저의 모든 할 일 목록을 조회합니다.
    화면: '나의 TODO' 탭 리스트업
    """
    tasks = service.get_my_tasks(db, TEST_USER_ID)
    # Schema에 정의된 리스트 구조로 변환하여 반환
    return {"items": [
    {
        "todo_id": str(t.id), 
        "task": t.name if t.name else "이름 없음",
        "is_completed": t.is_completed
    } for t in tasks
    ]}


@router.post("", status_code=201)
def create_todo(
    request: CreateToDoRequest,
    db: Session = Depends(get_db),
    service: TodoService = Depends(get_todo_service)
):
    """
    용도: 새로운 할 일을 직접 생성하거나 후보군에서 선택하여 등록합니다.
    로직: Task 생성 -> Todo 생성 순으로 진행됩니다.
    """
    return service.create_todo_from_candidate(
        db, 
        user_id=TEST_USER_ID,
        matching_id=UUID(request.matching_id),
        skill_id=UUID(request.skill_id),
        task_name=request.task
    )


@router.patch("/{task_id}")
def update_todo(
    task_id: UUID,
    request: UpdateToDoRequest,
    db: Session = Depends(get_db),
    service: TodoService = Depends(get_todo_service)
):
    """
    용도: 할 일의 완료 상태(체크박스)를 업데이트합니다.
    """
    updated = service.update_todo_status(db, TEST_USER_ID, task_id, request.is_completed)
    if not updated:
        raise HTTPException(status_code=404, detail="해당 태스크를 찾을 수 없습니다.")
    return {"message": "업데이트 성공"}


@router.get("/{matching_id}/opponent-tasks", response_model=ViewMyToDoResponse)
def get_opponent_tasks(
    matching_id: UUID,
    opponent_id: UUID, # 실제로는 매칭 정보를 통해 서버에서 조회해야 함
    db: Session = Depends(get_db),
    service: TodoService = Depends(get_todo_service)
):
    """
    용도: 매칭된 상대방의 투두 목록을 조회합니다.
    화면: '상대의 TODO' 탭 리스트업
    """
    tasks = service.get_opponent_tasks(db, matching_id, opponent_id)
    return {"items": [
        ToDoItem(todo_id=t.id, task=t.name, is_completed=t.is_completed) 
        for t in tasks
    ]}


# ---------------------------------------------------------
# 2. AI/채팅 추천 후보 Todo (GeneratedTodo)
# ---------------------------------------------------------

@router.post("/generated_todo", response_model=ViewToDoCandidateResponse)
def create_generated_todo(
    request: CreateToDoCandidateRequest,
    db: Session = Depends(get_db),
    service: TodoService = Depends(get_todo_service)
):
    """
    용도: 대화 로그를 기반으로 AI가 추천하는 투두 후보군을 생성합니다.
    """
    # 실제 구현 시에는 AI 로직 호출 후 repo.create_generated_todo 사용
    return {"candidates": []} 


@router.get("/generated_todo", response_model=ViewToDoCandidateResponse)
def get_generated_todo(
    chatroom_id: UUID,
    db: Session = Depends(get_db),
    service: TodoService = Depends(get_todo_service)
):
    """
    용도: 현재 채팅방에 추천된 투두 후보군 리스트를 가져옵니다.
    화면: 투두 추천 팝업 또는 커리큘럼 선택 창
    """
    candidates = service.get_candidates(db, chatroom_id)
    return {"candidates": [
        ToDoCandidate(id=str(c.chatroom_id), name=c.name, skill=str(c.skill_id)) 
        for c in candidates
    ]}