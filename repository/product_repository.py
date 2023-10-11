from database import SessionLocal
from models.product_model import Product


class ProductRepository:

    @staticmethod
    async def create_product(name, description, price, quantity, category_id):

        db_product = Product(name=name, description=description, price=price, quantity=quantity, category_id=category_id)

        db = SessionLocal()
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

