import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from controller.auth_controller import check_token_bearer
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from repository.user_repository import UserRepository
from schemas.category_schemas import CategoryCreate
from repository.category_repository import CategoryRepository


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()
router = APIRouter()


@router.post("/shop/category")
async def create_category(category: CategoryCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(category)
        user = await UserRepository.get_user_by_email(db, payload.get("user"))
        category_from_db = await CategoryRepository.get_category_by_name(db, category.name)

        if category_from_db:
            raise HTTPException(status_code=409, detail="Category with this name already exists")

        if user.role.name != "admin":
            raise HTTPException(status_code=403, detail="Access denied. You do not have administrator privileges.")

        category = await CategoryRepository.create_category(db, category.name)

        return category

    except HTTPException as http_error:
        raise http_error
    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))

