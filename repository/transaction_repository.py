from sqlalchemy import update

from models.transaction_model import Transaction
from sqlalchemy.orm import Session


class TransactionRepository:

    @staticmethod
    async def create_transaction(db: Session, user_id, cart_id, transaction_type):
        db_transaction = Transaction(user_id=user_id, cart_id=cart_id, transaction_type=transaction_type)

        db.add(db_transaction)
        db.commit()

        transaction = {
            "id": db_transaction.id,
            "cart_id": db_transaction.cart_id,
            "user_id": db_transaction.user_id,
            "status": db_transaction.status,
            "transaction_type": db_transaction.transaction_type

        }

        return transaction

    @staticmethod
    async def confirm(db: Session, transaction_id):
        statement = update(Transaction).filter(Transaction.id == transaction_id).values(status=True)
        db.execute(statement)
        db.commit()

    @staticmethod
    async def get_transaction_by_id(db: Session, user_id):

        transaction = db.query(Transaction).filter_by(user_id=user_id).first()
        return transaction

    @staticmethod
    async def get_transaction_by_cart_id(db: Session, cart_id):
        transaction = db.query(Transaction).filter_by(cart_id=cart_id).first()
        return transaction
