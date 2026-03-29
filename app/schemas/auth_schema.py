from pydantic import BaseModel

class UserInfo(BaseModel):
    {
    "email": str,
    "name": str,
    "password": str
}
    
class LoginRequest (BaseModel):
    email: str
    password: str
    
class LoginResponse(BaseModel):
    access_token: str
    token_type: str