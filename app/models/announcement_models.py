import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.types import Uuid

from app.models.base import Base


class Announcement(Base):
    __tablename__ = "ANNOUNCEMENT"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid, ForeignKey("USER.id"))
    want_to_skill = Column(Uuid, ForeignKey("SKILL.id", ondelete="CASCADE", onupdate="CASCADE"))
    can_teach_skill = Column(Uuid, ForeignKey("SKILL.id", ondelete="CASCADE", onupdate="CASCADE"))
    want_to_message = Column(Text)
    can_teach_message = Column(Text)
    can_teach_difficulty = Column(String(100))
    want_to_difficulty = Column(String(100))