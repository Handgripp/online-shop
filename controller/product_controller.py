from fastapi import APIRouter, HTTPException
from repository.category_repository import CategoryRepository
from schemas.product_schemas import ProductCreate
from repository.product_repository import ProductRepository

router = APIRouter()


@router.post("/shop/products")
async def create_product(product: ProductCreate):
    try:
        category = await CategoryRepository.get_category_by_id(product.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category id does not exists")

        new_product = await ProductRepository.create_product(product.name, product.description,
                                                                 product.price, product.quantity, product.category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

    return new_product
