from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from schemas.category_schemas import CategoryCreate
from repository.category_repository import CategoryRepository

router = APIRouter()


@router.post("/shop/category")
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        category = await CategoryRepository.create_category(db, category.name)

        return category

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
