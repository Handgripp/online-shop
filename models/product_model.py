import uuid
from sqlalchemy import Column, String, UUID, ForeignKey, Integer, DateTime, func, LargeBinary
from database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    filename = Column(String, unique=True, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

