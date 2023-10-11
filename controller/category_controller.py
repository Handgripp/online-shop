from fastapi import APIRouter, HTTPException

from schemas.category_schemas import CategoryCreate
from repository.category_repository import CategoryRepository

router = APIRouter()


@router.post("/shop/category")
async def create_category(category: CategoryCreate):

    category = await CategoryRepository.create_category(category.name)

    return category

