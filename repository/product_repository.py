from sqlalchemy import update

from database import SessionLocal
from models.product_model import Product
from sqlalchemy.orm import Session


class ProductRepository:

    @staticmethod
    async def create_product(db: Session, name, description, price, quantity, category_id):
        db_product = Product(name=name, description=description, price=price, quantity=quantity,
                             category_id=category_id)

        db.add(db_product)
        db.commit()

        product = {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "quantity": db_product.quantity,
            "category_id": db_product.category_id
        }

        return product

    @staticmethod
    async def get_product_by_id(db: Session, product_id):
        product = db.query(Product).filter_by(id=product_id).first()
        return product

    @staticmethod
    async def get_product_by_name(db: Session, product_name):
        product = db.query(Product).filter_by(name=product_name).first()
        return product


    @staticmethod
    async def update_cart_value(db: Session, updated_quantity, product_id):
        statement = update(Product).filter(Product.id == product_id).values(quantity=updated_quantity)
        db.execute(statement)
        db.commit()
