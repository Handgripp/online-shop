from fastapi import APIRouter, HTTPException
from models.user_model import RoleEnum
from schemas.user_schemas import UserCreate
from repository.user_repository import UserRepository

router = APIRouter()


@router.post("/users")
def create_user(user: UserCreate):
    role = None

    user_in_db = UserRepository.get_user_by_email(user.email)
    if user_in_db:
        raise HTTPException(status_code=409, detail="User with this email already exists")

    if user.role == "Client":
        role = RoleEnum.client
    elif user.role == "Admin":
        role = RoleEnum.admin

    user = UserRepository.create_user(user.email, user.password, role)

    return user

