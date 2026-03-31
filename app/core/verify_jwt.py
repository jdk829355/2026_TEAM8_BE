import os
from typing import Optional
from uuid import UUID

import dotenv
from fastapi import HTTPException, Header
from jwt import decode as jwt_decode, encode as jwt_encode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

dotenv.load_dotenv(".env.secret")  # .env.secret 파일에서 환경 변수 로드

SECRET_KEY = os.getenv("JWT_SECRET", "my_super_secret_key")
EMAIL_VERIFICATION_SECRET = os.getenv("JWT_EMAIL_VERIFICATION_SECRET", "my_email_verification_secret_key")
ALGORITHM = "HS256"


def get_current_user_id(Authorization: Optional[str] = Header(None)) -> UUID:
    if Authorization is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Bearer 스키마가 아닙니다.")
        
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        
        if user_id_str is None:
            raise HTTPException(status_code=401, detail="토큰에 ID가 없습니다.")
            
        return UUID(user_id_str)  # UUID 객체로 변환하여 반환

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
def get_email_from_verification_token(token: str):
    try:
        payload = jwt_decode(token, EMAIL_VERIFICATION_SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=400, detail="토큰에 이메일이 없습니다.")
            
        return email

    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="토큰이 만료되었습니다.")
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=400, detail="유효하지 않은 토큰입니다.")
    

def generate_jwt(user_id: str | UUID):
    payload = {"sub": str(user_id)}
    token = jwt_encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def generate_email_verification_token(email: str):
    payload = {"sub": email}
    token = jwt_encode(payload, EMAIL_VERIFICATION_SECRET, algorithm=ALGORITHM)
    return token