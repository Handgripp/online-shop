from models.category_model import Category
from sqlalchemy.orm import Session

class CategoryRepository:

    @staticmethod
    async def create_category(db: Session, name):

        db_category = Category(name=name)

        db.add(db_category)
        db.commit()

        category = {
            "id": db_category.id,
            "name": db_category.name
        }

        return category

    @staticmethod
    async def get_category_by_id(db: Session, category_id):

        category = db.query(Category).filter_by(id=category_id).first()
        return category

    @staticmethod
    async def get_category_by_name(db: Session, name):
        category = db.query(Category).filter_by(name=name).first()
        return category
