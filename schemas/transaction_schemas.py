from pydantic import BaseModel, UUID4


class TransactionCreate(BaseModel):
    transaction_type: str
    cart_id: UUID4

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaction_type": "Blik",
                    "cart_id": ""
                }
            ]
        }
    }
