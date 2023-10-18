from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import RoleEnum
from schemas.user_schemas import UserCreate
from repository.user_repository import UserRepository
from sqlalchemy.exc import DataError

router = APIRouter()


@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    role = None
    try:
        user_in_db = await UserRepository.get_user_by_email(db, user.email)
        if user_in_db is not None:
            raise HTTPException(status_code=409, detail="User with this email already exists")

        if user.role == "Client":
            role = RoleEnum.client
        elif user.role == "Admin":
            role = RoleEnum.admin

        user = await UserRepository.create_user(db, user.email, user.password, role)

        return user

    except HTTPException as http_error:
        raise http_error
    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))

