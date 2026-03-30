import re

from pydantic import BaseModel, field_validator

class CreateUserRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def validate_email(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("유효한 이메일 주소를 입력해주세요.")
        return value
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int