import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.types import Uuid

from app.models.base import Base


class Chatroom(Base):
    __tablename__ = "CHATROOM"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    matching_id = Column(Uuid, ForeignKey("MATCHING.id", ondelete="CASCADE"))
    announcement_id = Column(Uuid, ForeignKey("ANNOUNCEMENT.id"))
    user_id = Column(Uuid, ForeignKey("USER.id"))


class JoinChat(Base):
    __tablename__ = "JOIN_CHAT"

    user_id = Column(Uuid, ForeignKey("USER.id"), primary_key=True)
    room_id = Column(Uuid, ForeignKey("CHATROOM.id"), primary_key=True)


class MatchingRequest(Base):
    __tablename__ = "MATCHING_REQUEST"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    from_user_id = Column("from", Uuid, ForeignKey("USER.id"))
    to_user_id = Column("to", Uuid, ForeignKey("USER.id"))
    room_id = Column(Uuid, ForeignKey("CHATROOM.id"))


class ChatLog(Base):
    __tablename__ = "CHAT_LOG"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    author_id = Column(Uuid, ForeignKey("USER.id"))
    room_id = Column(Uuid, ForeignKey("CHATROOM.id", ondelete="SET NULL"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    read = Column(Boolean, default=False)


class ChatAnalysis(Base):
    __tablename__ = "CHAT_ANALYSIS"

    user_id = Column(Uuid, ForeignKey("USER.id"), primary_key=True)
    chatroom_id = Column(Uuid, ForeignKey("CHATROOM.id"), primary_key=True)
    matching_probability = Column(Float)
    message = Column(Text)
