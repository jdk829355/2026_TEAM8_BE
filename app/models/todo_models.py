import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.types import Uuid

from app.models.base import Base


class Task(Base):
    __tablename__ = "TASK"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    skill_id = Column(Uuid, ForeignKey("SKILL.id"))
    matching_id = Column(Uuid, ForeignKey("MATCHING.id"))
    user_id = Column(Uuid, ForeignKey("USER.id"))
    name = Column(String(255))
    is_completed = Column(Boolean, default=False)

    skill = relationship("Skill")


class GeneratedTodo(Base):
    __tablename__ = "GENERATED_TODO"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    chatroom_id = Column(Uuid, ForeignKey("CHATROOM.id"), primary_key=True)
    skill_id = Column(Uuid, ForeignKey("SKILL.id"), primary_key=True)
    created_at = Column(DateTime, primary_key=True)
    name = Column(Text)