from pydantic import BaseModel, EmailStr, validator, ValidationError
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

    @validator("password")
    def validate_password(cls, value):
        min_length = 8
        errors = []
        if len(value) < min_length:
            errors.append('Password must be at least 8 characters long.')
        if not any(char.isupper() for char in value):
            errors.append('Password should contain at least one uppercase character.')
        if not any(char.islower() for char in value):
            errors.append('Password should contain at least one lowercase character.')
        if not any(char.isdigit() for char in value):
            errors.append('Password should contain at least one digit.')
        if not any(char in "!@#$%^&*" for char in value):
            errors.append('Password should contain at least one of the following special characters: !@#$%^&*')
        if errors:
            raise ValueError(errors)

        return value

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
