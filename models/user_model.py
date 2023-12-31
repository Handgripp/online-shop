import uuid
from enum import Enum
from sqlalchemy import Column, String, UUID, DateTime, func
from database import Base
from sqlalchemy.dialects.postgresql import ENUM


class RoleEnum(Enum):
    admin = 'Admin'
    client = 'Client'


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(ENUM(RoleEnum))
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())



