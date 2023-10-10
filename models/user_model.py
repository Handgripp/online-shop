from enum import Enum
from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.dialects.postgresql import ENUM


class RoleEnum(Enum):
    admin = 'Admin'
    client = 'Client'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(ENUM(RoleEnum))



