import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from controller.auth import check_token_bearer
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from repository.category_repository import CategoryRepository
from repository.user_repository import UserRepository
from schemas.product_schemas import ProductCreate
from repository.product_repository import ProductRepository

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()
router = APIRouter()


@router.post("/shop/products")
async def create_product(product: ProductCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        category = await CategoryRepository.get_category_by_name(db, product.category_name)
        user = await UserRepository.get_user_by_email(db, payload.get("user"))

        if user.role.name != "admin":
            raise HTTPException(status_code=403, detail="Access denied. You do not have administrator privileges.")

        if not category:
            raise HTTPException(status_code=404, detail="Category name does not exists")

        new_product = await ProductRepository.create_product(db, product.name, product.description,
                                                             product.price, product.quantity, category.id)

        return new_product

    except HTTPException as http_error:
        raise http_error

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))



