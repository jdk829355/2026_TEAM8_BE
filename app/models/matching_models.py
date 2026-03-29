import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.types import Uuid

from app.models.base import Base


class Matching(Base):
    __tablename__ = "MATCHING"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255))


class Teach(Base):
    __tablename__ = "TEACH"

    teacher_id = Column(Uuid, ForeignKey("USER.id"), primary_key=True)
    skill_id = Column(Uuid, ForeignKey("SKILL.id"), primary_key=True)
    matching_id = Column(Uuid, ForeignKey("MATCHING.id"), primary_key=True)
    status = Column(String(100))