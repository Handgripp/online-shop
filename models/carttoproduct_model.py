import uuid
from sqlalchemy import Column, UUID, ForeignKey, Integer
from database import Base


class CartToProduct(Base):
    __tablename__ = "CartToProducts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    cart_id = Column(UUID(as_uuid=True), ForeignKey('carts.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    quantity = Column(Integer)

