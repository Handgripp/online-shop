from pydantic import BaseModel, validator
# from models.transaction_model import TransactionEnum


class TransactionCreate(BaseModel):
    transaction_type: str

    # @validator("transaction_type")
    # def validate_transaction(cls, transaction_type):
    #     allowed_transactions = []
    #     for enum_value in TransactionEnum:
    #         allowed_transactions.append(enum_value.value)
    #     if transaction_type not in allowed_transactions:
    #         raise ValueError(f"Invalid transaction. Allowed transactions are: {', '.join(allowed_transactions)}")
    #     return transaction_type

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaction_type": "Blik",
                }
            ]
        }
    }
