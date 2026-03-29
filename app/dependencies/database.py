import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging  

load_dotenv(".env.secret")

logger = logging.getLogger(__name__)

DATABASE_URL = str(os.getenv(
    "DATABASE_URL"
))

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# DB 세션 의존성 (Router에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()