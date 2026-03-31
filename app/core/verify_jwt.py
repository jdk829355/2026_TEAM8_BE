import os
from typing import Optional
from uuid import UUID

import dotenv
from fastapi import HTTPException, Header, Query
from jwt import decode as jwt_decode, encode as jwt_encode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

dotenv.load_dotenv(".env.secret")  # .env.secret 파일에서 환경 변수 로드

SECRET_KEY = os.getenv("JWT_SECRET", "my_super_secret_key")
EMAIL_VERIFICATION_SECRET = os.getenv("JWT_EMAIL_VERIFICATION_SECRET", "my_email_verification_secret_key")
ALGORITHM = "HS256"


def get_current_user_id(Authorization: Optional[str] = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Bearer 스키마가 아닙니다.")
        
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰에 ID가 없습니다.")
            
        return user_id # 여기서는 string 형태의 UUID가 리턴됨

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
def get_current_user_id_ws(token: str = Query(None, alias="token")):
    if token is None:
        raise HTTPException(status_code=401, detail="인증 헤더가 필요합니다.")
    
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰에 ID가 없습니다.")
            
        return user_id # 여기서는 string 형태의 UUID가 리턴됨

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