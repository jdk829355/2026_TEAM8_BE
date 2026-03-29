from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/send_email")
def send_email():
    return {"message": "send_email handler"}


@router.get("/verify_email")
def verify_email():
    return {"message": "verify_email handler"}


@router.post("/user/register")
def register_user():
    return {"message": "register_user handler"}


@router.post("/login")
def login():
    return {"message": "login handler"}
