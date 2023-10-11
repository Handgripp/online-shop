import uuid
from sqlalchemy import Column, String, UUID, ForeignKey, Integer
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
