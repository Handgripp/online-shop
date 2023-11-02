import uuid
from enum import Enum
from sqlalchemy import Column, UUID, ForeignKey, Boolean, String
from database import Base
from sqlalchemy.dialects.postgresql import ENUM


# class TransactionEnum(Enum):
#     card = 'Card'
#     blik = 'Blik'
#     transfer = 'Transfer'


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    cart_id = Column(UUID(as_uuid=True), ForeignKey('carts.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    is_paid = Column(Boolean, default=False)
    transaction_type = Column(String)
