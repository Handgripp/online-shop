import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from controller.auth_controller import check_token_bearer
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from repository.cart_repository import CartRepository
from repository.category_repository import CategoryRepository
from repository.notification_repository import NotificationRepository
from repository.user_repository import UserRepository
from schemas.product_schemas import ProductCreate, AddProductToCart
from repository.product_repository import ProductRepository
from services.mailer import queue, send_email


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()
router = APIRouter()


@router.post("/shop/products")
async def create_product(add_product_to_db: ProductCreate, db: Session = Depends(get_db),
                         credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        category = await CategoryRepository.get_category_by_name(db, add_product_to_db.category_name)
        user = await UserRepository.get_user_by_email(db, payload.get("user"))

        if user.role.name != "admin":
            raise HTTPException(status_code=403, detail="Access denied. You do not have administrator privileges.")

        if not category:
            raise HTTPException(status_code=404, detail="Category name does not exists")

        new_product = await ProductRepository.create_product(db, add_product_to_db.name, add_product_to_db.description,
                                                             add_product_to_db.price, add_product_to_db.quantity,
                                                             category.id)

        return new_product

    except HTTPException as http_error:
        raise http_error

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))


@router.post("/shop/carts")
async def create_cart(db: Session = Depends(get_db),
                      credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await UserRepository.get_user_by_email(db, payload.get("user"))
        cart_id = await CartRepository.get_cart_by_user_id(db, user.id)
        if cart_id:
            raise HTTPException(status_code=400, detail="You already have one cart")

        cart = await CartRepository.create_cart(db, user.id)
        return cart

    except HTTPException as http_error:
        raise http_error

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))


@router.post("/shop/carts/<cart_id>/assign-product")
async def add_products_to_cart(cart_id: str, purchased_products: AddProductToCart, db: Session = Depends(get_db),
                               credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        product = await ProductRepository.get_product_by_name(db, purchased_products.product_name)
        user = await UserRepository.get_user_by_email(db, payload.get("user"))
        cart = await CartRepository.get_cart_by_id(db, cart_id)

        if not product.quantity >= purchased_products.quantity:
            await NotificationRepository.create_notification(db, user.id, product.id)
            raise HTTPException(status_code=400, detail="Not enough quantity of this product available, we will "
                                                        "send you an email when it becomes available")

        product_to_cart = await CartRepository.add_products_to_cart(db, cart.id,
                                                                    product.id,
                                                                    purchased_products.quantity)

        product_value_to_cart = (product.price * purchased_products.quantity) + cart.value

        updated_quantity = product.quantity - purchased_products.quantity

        await ProductRepository.update_cart_value(db, updated_quantity, product.id)
        await CartRepository.update_cart_value(db, product_value_to_cart, user.id)

        return product_to_cart

    except HTTPException as http_error:
        raise http_error

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))


@router.get("/shop/products/check-products")
async def check_products(db: Session = Depends(get_db)):
    notifications = await NotificationRepository.get_all_notification(db)
    for notification in notifications:
        product_to_check = await asyncio.to_thread(ProductRepository.get_product_by_id, db, notification.product_id)
        if product_to_check.quantity > 0:
            user = await UserRepository.get_user_by_id(db, notification.user_id)
            queue.enqueue(send_email, user.email, "The product you couldn't buy is back in the store",
                          f"You can buy {product_to_check.name}")
            await NotificationRepository.confirm(db, notification.id)
            if notification.send is True:
                await NotificationRepository.delete(db, notification.id)
