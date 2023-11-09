import uuid
from sqlalchemy import Column, UUID, ForeignKey, Integer, DateTime, func
from database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    value = Column(Integer, default=0)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
