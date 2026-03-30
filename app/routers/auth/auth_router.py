import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse

from app.core.dependencies import get_auth_service
from app.dependencies.database import get_db
from app.core.verify_jwt import generate_email_verification_token, generate_jwt, get_current_user_id, get_email_from_verification_token
from app.dependencies.email import send_email
from app.models.user_models import User
from app.schemas.auth_schema import CreateUserRequest, LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/create_user")
def create_user(create_user_request: CreateUserRequest, service: AuthService = Depends(get_auth_service), db=Depends(get_db)):
    logger = logging.getLogger(__name__)
    if service.is_email_duplicated(db=db, email=create_user_request.email):
        logger.error(f"Email already exists: {create_user_request.email}")
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
    
    try:
        service.create_user(db=db, create_user_request=create_user_request)
    except Exception as e:
        logger.error(f"Error occurred while creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"사용자 생성 실패: {str(e)}")
    return {"message": "사용자가 성공적으로 생성되었습니다."}

@router.get("/send_email")
def send_email_endpoint(email: str, service: AuthService = Depends(get_auth_service), db=Depends(get_db)):
    logger = logging.getLogger(__name__)

    if not service.is_email_duplicated(db=db, email=email):
        logger.error(f"Email does not exist: {email}")
        raise HTTPException(status_code=400, detail="존재하지 않는 이메일입니다.")

    if service.check_email_verification(db=db, email=email):
        logger.error(f"Email already verified: {email}")
        raise HTTPException(status_code=400, detail="이미 인증된 이메일입니다.")
    
    token = generate_email_verification_token(email)

    try:
        send_email(email=email, token=token)
    except Exception as e:
        logger.error(f"Error occurred while sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"이메일 전송 실패")
    return


@router.get("/verify_email")
def verify_email(token: str, service: AuthService = Depends(get_auth_service), db=Depends(get_db)):
    logger = logging.getLogger(__name__)
    try:
        email = get_email_from_verification_token(token)
    except HTTPException as e:
        logger.error(f"Error occurred while verifying email: {str(e)}")
        with open("app/templates/email_verification_failed.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=e.status_code)
    
    if (user_id := service.get_user_by_email(db=db, email=email)) is None:
        logger.error(f"User not found for email: {email}")
        raise HTTPException(status_code=400, detail="존재하지 않는 이메일입니다.")

    try:
        user_id = service.update_user_verification(db=db,user_id= user_id.id,is_verified=True)
    except Exception as e:
        logger.error(f"Error occurred while verifying email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"이메일 인증 실패")

    with open("app/templates/email_verified.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@router.patch("/user_info")
def update_user_info():
    return {"message": "update_user_info handler"}


@router.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest, service: AuthService = Depends(get_auth_service), db=Depends(get_db)):
    user:User = service.get_user_by_email(db=db, email=login_request.email)
    if user is None:
        raise HTTPException(status_code=400, detail="존재하지 않는 이메일입니다.")
    
    if not service.verify_password(login_request.password, user.password): # type: ignore
        raise HTTPException(status_code=400, detail="잘못된 비밀번호입니다.")
    
    if not user.is_verified: # type: ignore
        raise HTTPException(status_code=400, detail="이메일 인증이 필요합니다.")
    
    return LoginResponse(
        access_token=generate_jwt(user_id=user.id), # type: ignore
        token_type="bearer",
        expires_in=3600
    )