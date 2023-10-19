from models.cart_model import Cart
from sqlalchemy.orm import Session


class CartRepository:

    @staticmethod
    async def create_cart(db: Session, value, user_id):

        db_cart = Cart(value=value, user_id=user_id)

        db.add(db_cart)
        db.commit()

        cart = {
            "id": db_cart.id,
            "value": db_cart.value,
            "user_id": db_cart.user_id
        }

        return cart

    @staticmethod
    async def get_cart_by_user_id(db: Session, user_id):

        cart = db.query(Cart).filter_by(user_id=user_id).first()
        return cart
