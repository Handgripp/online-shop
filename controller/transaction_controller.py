import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from controller.auth import check_token_bearer
from controller.mailer import queue, send_email
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from repository.transaction_repository import TransactionRepository
from repository.user_repository import UserRepository
from repository.cart_repository import CartRepository
from schemas.transaction_schemas import TransactionCreate

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()
router = APIRouter()


@router.post("/shop/transactions")
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db),
                             credentials: HTTPAuthorizationCredentials = Security(security),
                             expires_delta: timedelta = None):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await UserRepository.get_user_by_email(db, payload.get("user"))
        cart_id = await CartRepository.get_cart_by_user_id(db, user.id)

        await TransactionRepository.create_transaction(db, user.id, cart_id.id, transaction.transaction_type)

        to_encode = {"exp": expires_delta, "id": str(user.id)}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        queue.enqueue(send_email, user.email, "Confirm your purchase in the store", f"http://127.0.0.1:8000/shop"
                                                                                    f"/transactions/payment"
                                                                                    f"-confirmation/{encoded_jwt}")

        raise HTTPException(status_code=200, detail="Send message to your email")

    except HTTPException as http_error:
        raise http_error
    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))


@router.get("/shop/transactions/payment-confirmation/{token}")
async def confirm_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await UserRepository.get_user_by_id(db, payload.get("id"))
        transaction = await TransactionRepository.get_transaction_by_id(db, user.id)

        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")

        await TransactionRepository.confirm(db, transaction.id)

        return {"message": "Transaction confirmed"}

    except HTTPException as http_error:
        raise http_error

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))
