import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.types import Uuid

from app.models.base import Base


class Task(Base):
    __tablename__ = "TASK"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    skill_id = Column(Uuid, ForeignKey("SKILL.id"))
    matching_id = Column(Uuid, ForeignKey("MATCHING.id"))
    name = Column(String(255))


class Todo(Base):
    __tablename__ = "TODO"

    user_id = Column(Uuid, ForeignKey("USER.id"), primary_key=True)
    task_id = Column(Uuid, ForeignKey("TASK.id"), primary_key=True)
    skill_id = Column(Uuid, ForeignKey("TASK.skill_id"), primary_key=True)
    matching_id = Column(Uuid, ForeignKey("TASK.matching_id"), primary_key=True)
    is_completed = Column(Boolean, default=False)


class GeneratedTodo(Base):
    __tablename__ = "GENERATED_TODO"

    chatroom_id = Column(Uuid, ForeignKey("CHATROOM.id"), primary_key=True)
    name = Column(Text)
