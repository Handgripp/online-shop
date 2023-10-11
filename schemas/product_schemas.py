from pydantic import BaseModel, UUID4


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    quantity: int
    category_id: UUID4

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "KTM",
                    "description": "Fast",
                    "price": 120,
                    "quantity": 12,
                    "category_id": "1d153db3-201b-4e77-a5b3-b2d8b4a58df8"
                }
            ]
        }
    }
