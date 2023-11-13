from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from models.notification_model import Notification


class NotificationRepository:

    @staticmethod
    async def create_notification(db: Session, user_id, product_id):
        db_product = Notification(user_id=user_id, product_id=product_id)
        db.add(db_product)
        db.commit()

        return db_product

    @staticmethod
    async def get_all_notification(db: Session):
        transaction = db.query(Notification).all()
        return transaction

    @staticmethod
    async def confirm(db: Session, notification_id):
        statement = update(Notification).filter(Notification.id == notification_id).values(send=True)
        db.execute(statement)
        db.commit()

    @staticmethod
    async def delete(db: Session, notification_id):
        statement = delete(Notification).where(Notification.id == notification_id)
        db.execute(statement)
        db.commit()

    @staticmethod
    async def get_notifications_where_send_false(db: Session):
        transaction = db.query(Notification).filter_by(send=False).all()
        return transaction
