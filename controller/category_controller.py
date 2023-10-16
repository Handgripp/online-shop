from fastapi import APIRouter, HTTPException

from schemas.category_schemas import CategoryCreate
from repository.category_repository import CategoryRepository

router = APIRouter()


@router.post("/shop/category")
async def create_category(category: CategoryCreate):
    try:
        category = await CategoryRepository.create_category(category.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

    return category

