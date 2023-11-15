from pydantic import BaseModel


class AddProductToCart(BaseModel):
    product_name: str
    quantity: int

    model_config = {
        "json_schema_extra": {
            "examples": [

                {
                    "product_name": "KTM",
                    "quantity": 1
                }

            ]
        }
    }
