import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, Security, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from controller.auth_controller import check_token_bearer
from services.mailer import queue, send_email
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from repository.transaction_repository import TransactionRepository
from repository.user_repository import UserRepository
from repository.cart_repository import CartRepository
from schemas.transaction_schemas import TransactionCreate
from services.encoder import encode

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()
router = APIRouter()


@router.post("/shop/transactions")
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db),
                             credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        check_token_bearer(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await UserRepository.get_user_by_email(db, payload.get("user"))
        cart_id = await CartRepository.get_cart_by_id(db, transaction.cart_id)

        if not cart_id:
            raise HTTPException(status_code=404, detail="Cart not found")

        transaction_db = await TransactionRepository.get_transaction_by_id(db, user.id)

        if transaction_db:
            encoded_jwt = encode(user.id)
            queue.enqueue(send_email, user.email, "Confirm your purchase in the store",
                          f"You cannot initiate a new transaction until the existing one has been paid for. "
                          f"Pay now, click a link: http://127.0.0.1:8000/shop"
                          f"/transactions/payment"
                          f"-confirmation/{encoded_jwt}")

            raise HTTPException(status_code=200, detail="Send message to your email")

        await TransactionRepository.create_transaction(db, user.id, cart_id.id, transaction.transaction_type)

        encoded_jwt = encode(user.id)

        queue.enqueue(send_email, user.email, "Confirm your purchase in the store",
                      f"Pay now, click a link: "
                      f"http://127.0.0.1:8000/shop/transactions/payment-confirmation?token={encoded_jwt}")

        raise HTTPException(status_code=200, detail="Send message to your email")

    except HTTPException as http_error:
        raise http_error
    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))


@router.get("/shop/transactions/payment-confirmation/")
async def confirm_email(token: str = Query(...), db: Session = Depends(get_db)):
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
