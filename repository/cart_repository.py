from sqlalchemy import update

from models.cart_model import Cart
from models.carttoproduct_model import CartToProduct
from sqlalchemy.orm import Session


class CartRepository:

    @staticmethod
    async def create_cart(db: Session, user_id):

        db_cart = Cart(user_id=user_id)

        db.add(db_cart)
        db.commit()

        cart = {
            "id": db_cart.id,
            "value": 0,
            "user_id": db_cart.user_id
        }

        return cart

    @staticmethod
    async def update_cart_value(db: Session, new_value, user_id):
        statement = update(Cart).filter(Cart.user_id == user_id).values(value=new_value)
        db.execute(statement)
        db.commit()

    @staticmethod
    async def get_cart_by_user_id(db: Session, user_id):
        cart = db.query(Cart).filter_by(user_id=user_id).first()
        return cart

    @staticmethod
    async def get_cart_by_id(db: Session, cart_id):
        cart = db.query(Cart).filter_by(id=cart_id).first()
        return cart

    @staticmethod
    async def get_all_carts_by_user_id(db: Session, user_id):
        cart = db.query(Cart).filter_by(user_id=user_id).all()
        return cart

    @staticmethod
    async def add_products_to_cart(db: Session, cart_id, product_id, quantity):
        db_cart = CartToProduct(cart_id=cart_id, product_id=product_id, quantity=quantity)

        db.add(db_cart)
        db.commit()

        cart = {
            "id": db_cart.id,
            "cart_id": db_cart.cart_id,
            "product_id": db_cart.product_id,
            "quantity": db_cart.quantity
        }

        return cart

