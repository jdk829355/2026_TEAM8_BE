from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.models.todo_models import  Task, GeneratedTodo

class TodoRepository:

    # ---------------------------------------------------------
    # [조회] 사용자 기반 데이터 검색
    # ---------------------------------------------------------

    # 용도: 유저가 참여 중인 모든 매칭을 통틀어 "그 유저가 할 모든 일"을 리스트로 가져올 때 사용 (전체 대시보드용)
    # def get_todos_by_user(self, db: Session, user_id: uuid.UUID):
    #     return db.query(Todo).filter(Todo.user_id == user_id).all()
    #
    # # 용도: 특정 매칭 방 안에서 "나" 또는 "상대방"의 투두 리스트만 쏙 골라올 때 사용 (매칭 상세 페이지용)
    # def get_todos_by_matching_user(self, db: Session, matching_id: uuid.UUID, user_id: uuid.UUID):
    #     return db.query(Todo).filter(
    #         Todo.matching_id == matching_id,
    #         Todo.user_id == user_id
    #     ).all()
    #
    # # ---------------------------------------------------------
    # # [생성] 할 일 데이터 등록 (Task -> Todo 순서로 생성 필수)
    # # ---------------------------------------------------------
    #
    # # 용도: 실제 투두의 '내용'이 담긴 본체(Task)를 먼저 생성할 때 사용 (투두 생성의 1단계)
    # def create_task(self, db: Session, name: str, skill_id: uuid.UUID, matching_id: uuid.UUID):
    #     db_task = Task(
    #         id=uuid.uuid4(),
    #         name=name,
    #         skill_id=skill_id,
    #         matching_id=matching_id
    #     )
    #     db.add(db_task)
    #     db.commit()
    #     db.refresh(db_task)
    #     return db_task
    #
    # # 용도: 생성된 Task를 특정 유저와 연결하여 "실제 할 일 목록"에 등록할 때 사용 (투두 생성의 2단계 / 후보 채택 시 사용)
    # def create_todo(self, db: Session, user_id: uuid.UUID, task_id: uuid.UUID, skill_id: uuid.UUID, matching_id: uuid.UUID):
    #     db_todo = Todo(
    #         user_id=user_id,
    #         task_id=task_id,
    #         skill_id=skill_id,
    #         matching_id=matching_id,
    #         is_completed=False
    #     )
    #     db.add(db_todo)
    #     db.commit()
    #     db.refresh(db_todo)
    #     return db_todo
    #
    # # ---------------------------------------------------------
    # # [업데이트] 상태 변경
    # # ---------------------------------------------------------
    #
    # # 용도: 화면에서 체크박스를 눌렀을 때, '완료' 또는 '미완료' 상태를 DB에 반영할 때 사용
    # def update_todo_status(self, db: Session, user_id: uuid.UUID, task_id: uuid.UUID, is_completed: bool):
    #     todo = db.query(Todo).filter(
    #         Todo.user_id == user_id,
    #         Todo.task_id == task_id
    #     ).first() # 복합키(user+task)를 통해 딱 하나의 투두만 집어내어 수정
    #
    #     if todo:
    #         todo.is_completed = is_completed # type: ignore
    #         db.commit()
    #         db.refresh(todo)
    #     return todo
    #
    # # ---------------------------------------------------------
    # # [후보군 관리] AI 추천/채팅 기반 임시 투두 (GeneratedTodo)
    # # ---------------------------------------------------------

    # 용도: 채팅 로그 분석 결과로 나온 '추천 커리큘럼'들을 임시 저장소에 쌓아둘 때 사용
    def create_generated_todo(self, db: Session, chatroom_id: uuid.UUID, content: str, skill_id: uuid.UUID, created_at: datetime):
        db_gen = GeneratedTodo(
            chatroom_id=chatroom_id,
            name=content,
            skill_id=skill_id,
            created_at=created_at
        )
        
        db.add(db_gen)
        db.commit()
        db.refresh(db_gen)
        return db_gen

    # 용도: 사용자가 매칭 방에 들어왔을 때, 아직 채택되지 않은 '추천 투두 목록'을 보여줄 때 사용
    def get_generated_todos_by_chatroom(self, db: Session, chatroom_id: uuid.UUID):
        return db.query(GeneratedTodo).filter(GeneratedTodo.chatroom_id == chatroom_id).all()

    # 용도: 사용자가 추천 후보를 채택하여 실제 투두로 옮겼거나, 추천 목록을 거절/초기화할 때 임시 데이터를 비우기 위해 사용
    def delete_generated_todo(self, db: Session, chatroom_id: uuid.UUID):
        db.query(GeneratedTodo).filter(GeneratedTodo.chatroom_id == chatroom_id).delete()
        db.commit()