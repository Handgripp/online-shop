from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DataError
from repository.category_repository import CategoryRepository
from schemas.product_schemas import ProductCreate
from repository.product_repository import ProductRepository

router = APIRouter()


@router.post("/shop/products")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        category = await CategoryRepository.get_category_by_id(db, product.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category id does not exists")

        new_product = await ProductRepository.create_product(db, product.name, product.description,
                                                             product.price, product.quantity, product.category_id)

        return new_product

    except DataError as e:
        raise HTTPException(status_code=400, detail="Invalid data: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))


