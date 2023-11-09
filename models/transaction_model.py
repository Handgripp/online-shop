import uuid
from sqlalchemy import Column, UUID, ForeignKey, Boolean, String, DateTime, func
from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    cart_id = Column(UUID(as_uuid=True), ForeignKey('carts.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    status = Column(Boolean, default=False)
    transaction_type = Column(String)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
