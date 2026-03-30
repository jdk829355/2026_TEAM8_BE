from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import CreateUserRequest
from passlib.context import CryptContext


class AuthService:
    def __init__(self, repo: AuthRepository):
        self.repo = repo
        # bcrypt has a 72-byte input limit; bcrypt_sha256 avoids this while remaining compatible.
        self.password_context = CryptContext(
            schemes=["bcrypt_sha256", "bcrypt"],
            deprecated="auto",
        )

    def hash_password(self, plain_password: str) -> str:
        return self.password_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(plain_password, hashed_password)

    def create_user(self, db, create_user_request: CreateUserRequest):
        # Hash the password before storing it
        create_user_request.password = self.hash_password(create_user_request.password)
        return self.repo.create_user(db, create_user_request.model_dump())
    
    def get_user_by_id(self, db, user_id):
        return self.repo.get_user_by_id(db, user_id)
    
    def get_user_by_email(self, db, email):
        return self.repo.get_user_by_email(db, email)
    
    def update_user_verification(self, db, user_id, is_verified):
        return self.repo.update_user_verification(db, user_id, is_verified)
    
    def check_email_verification(self, db, email) -> bool:
        user = self.repo.get_user_by_email(db, email)
        if user is None:
            return False
        return bool(user.is_verified)
    
    def is_email_duplicated(self, db, email) -> bool:
        return self.repo.is_email_duplicated(db, email)
    
    def update_user_info(self, db, user_id, payload):
        payload = {
            "description": payload.get("description"),
            "passion": payload.get("passion"),
            "speech": payload.get("speech"),
            "purpose": payload.get("purpose"),
        }
        return self.repo.update_user(db, user_id, payload)