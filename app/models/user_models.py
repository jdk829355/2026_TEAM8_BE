import uuid

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.types import Uuid

from app.models.base import Base


class User(Base):
    __tablename__ = "USER"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(Text)
    email = Column(String(255))
    description = Column(Text)
    passion = Column(Integer)
    speech = Column(Integer)
    purpose = Column(Integer)
