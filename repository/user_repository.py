from database import SessionLocal
from models.user_model import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:

    @staticmethod
    async def create_user(email, password, role):
        hashed_password = pwd_context.hash(password)

        db_user = User(email=email, password=hashed_password, role=role)

        db = SessionLocal()
        db.add(db_user)
        db.commit()

        user = {
            "id": db_user.id,
            "email": db_user.email,
            "role": db_user.role
        }

        return user

    @staticmethod
    async def get_user_by_email(email):
        db = SessionLocal()
        user = db.query(User).filter_by(email=email).first()
        return user
