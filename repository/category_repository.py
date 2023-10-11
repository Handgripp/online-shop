from database import SessionLocal
from models.category_model import Category


class CategoryRepository:

    @staticmethod
    async def create_category(name):

        db_category = Category(name=name)

        db = SessionLocal()
        db.add(db_category)
        db.commit()

        category = {
            "id": db_category.id,
            "name": db_category.name
        }

        return category

    @staticmethod
    async def get_category_by_id(category_id):
        db = SessionLocal()
        category = db.query(Category).filter_by(id=category_id).first()
        return category
