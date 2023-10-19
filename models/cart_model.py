import uuid
from sqlalchemy import Column, UUID, ForeignKey, Integer
from database import Base


class Carts(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    value = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
