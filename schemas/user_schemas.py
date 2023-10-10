from pydantic import BaseModel, EmailStr, validator
from models.user_model import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

    @validator("role")
    def validate_role(cls, role):
        allowed_roles = []
        for enum_value in RoleEnum:
            allowed_roles.append(enum_value.value)
        if role not in allowed_roles:
            raise ValueError(f"Invalid role. Allowed roles are: {', '.join(allowed_roles)}")
        return role

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "test@test.com",
                    "password": "12345",
                    "role": "Client"
                }
            ]
        }
    }
