from pydantic import BaseModel, UUID4


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "KTM",
                    "description": "Fast",
                    "price": 120,
                    "quantity": 12,
                    "category_name": "Cross"
                }
            ]
        }
    }


class AddProductToCart(BaseModel):
    product_name: str
    cart_id: UUID4
    quantity: int

    model_config = {
        "json_schema_extra": {
            "examples": [

                {
                    "product_name": "KTM",
                    "quantity": 1,
                    "cart_id": ""
                }

            ]
        }
    }
