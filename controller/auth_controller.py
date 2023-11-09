import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta
from jose import jwt, JWTError
from repository.user_repository import UserRepository
from schemas.auth_schemas import UserAuth

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_token_bearer(token, db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = UserRepository.get_user_by_email(db, payload.get("user"))
        if not user:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        expiration_timestamp = payload.get("exp")
        if expiration_timestamp is None:

            raise HTTPException(status_code=401, detail="Token has no expiration time")

        current_timestamp = datetime.timestamp(datetime.utcnow())

        if current_timestamp > expiration_timestamp:
            raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
async def login(user: UserAuth, db: Session = Depends(get_db)):
    try:
        if not user.email or not user.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")

        user_db = await UserRepository.get_user_by_email(db, user.email)

        if not user_db or pwd_context.verify(user.password, user_db.password) is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token}
    except HTTPException as http_error:
        raise http_error
    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))
