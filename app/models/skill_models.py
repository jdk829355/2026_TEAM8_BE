import uuid

from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.types import Uuid

from app.models.base import Base


class Skill(Base):
    __tablename__ = "SKILL"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False, index=True)
    category = Column(Text, nullable=False, index=True)


class Want(Base):
    __tablename__ = "WANT"

    user_id = Column(Uuid, ForeignKey("USER.id"), primary_key=True)
    skill_id = Column(Uuid, ForeignKey("SKILL.id"), primary_key=True)


class CanTeach(Base):
    __tablename__ = "CAN_TEACH"

    skill_id = Column(Uuid, ForeignKey("SKILL.id"), primary_key=True)
    user_id = Column(Uuid, ForeignKey("USER.id"), primary_key=True)
