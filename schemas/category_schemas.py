from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Cross",
                }
            ]
        }
    }
