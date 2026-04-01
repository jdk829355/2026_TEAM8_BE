import os
from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, declarative_base
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

def init_db():
    db = SessionLocal()
    try:
        db.execute(text("""
            /* Skill 테이블 데이터 마이그레이션 스크립트 */

        -- 1. (참고) 테이블이 없는 경우를 대비한 스키마 생성 
        -- CREATE TABLE IF NOT EXISTS Skill (
        --     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        --     name VARCHAR(100) NOT NULL,
        --     category VARCHAR(100) NOT NULL
        -- );

        -- 2. 스킬 데이터 삽입
        INSERT INTO Skill (id, name, category) VALUES
        -- 개발
        (gen_random_uuid(), '파이썬', '개발'),
        (gen_random_uuid(), '리액트', '개발'),
        (gen_random_uuid(), '클라우드', '개발'),
        (gen_random_uuid(), '데이터', '개발'),
        (gen_random_uuid(), '인공지능', '개발'),
        (gen_random_uuid(), '보안', '개발'),
        (gen_random_uuid(), '인프라', '개발'),
        (gen_random_uuid(), '웹', '개발'),
        (gen_random_uuid(), '앱', '개발'),

        -- 디자인
        (gen_random_uuid(), '피그마', '디자인'),
        (gen_random_uuid(), '영상', '디자인'),
        (gen_random_uuid(), '브랜딩', '디자인'),
        (gen_random_uuid(), '입체', '디자인'),
        (gen_random_uuid(), '설계', '디자인'),
        (gen_random_uuid(), '포토샵', '디자인'),
        (gen_random_uuid(), '일러스트', '디자인'),

        -- 비즈니스
        (gen_random_uuid(), '마케팅', '비즈니스'),
        (gen_random_uuid(), '기획', '비즈니스'),
        (gen_random_uuid(), '전략', '비즈니스'),
        (gen_random_uuid(), '영업', '비즈니스'),
        (gen_random_uuid(), '분석', '비즈니스'),
        (gen_random_uuid(), '제휴', '비즈니스'),
        (gen_random_uuid(), '그로스', '비즈니스'),

        -- 자기계발
        (gen_random_uuid(), '노션', '자기계발'),
        (gen_random_uuid(), '생산성', '자기계발'),
        (gen_random_uuid(), '영어', '자기계발'),
        (gen_random_uuid(), '소통', '자기계발'),
        (gen_random_uuid(), '리더십', '자기계발'),
        (gen_random_uuid(), '글쓰기', '자기계발'),
        (gen_random_uuid(), '독서', '자기계발'),

        -- 커리어
        (gen_random_uuid(), '이직', '커리어'),
        (gen_random_uuid(), '면접', '커리어'),
        (gen_random_uuid(), '이력서', '커리어'),
        (gen_random_uuid(), '포트폴리오', '커리어'),
        (gen_random_uuid(), '창업', '커리어'),
        (gen_random_uuid(), '인맥', '커리어'),
        (gen_random_uuid(), '코칭', '커리어'),

        -- 금융
        (gen_random_uuid(), '주식', '금융'),
        (gen_random_uuid(), '부동산', '금융'),
        (gen_random_uuid(), '코인', '금융'),
        (gen_random_uuid(), '회계', '금융'),
        (gen_random_uuid(), '세무', '금융'),
        (gen_random_uuid(), '재테크', '금융'),
        (gen_random_uuid(), '경제', '금융'),

        -- 라이프
        (gen_random_uuid(), '운동', '라이프'),
        (gen_random_uuid(), '사진', '라이프'),
        (gen_random_uuid(), '심리', '라이프'),
        (gen_random_uuid(), '여행', '라이프'),
        (gen_random_uuid(), '음악', '라이프'),
        (gen_random_uuid(), '요리', '라이프'),
        (gen_random_uuid(), '명상', '라이프');

        -- 작업 완료 확인
        SELECT * FROM Skill ORDER BY category, name;
"""))
    except Exception as e:
        logger.error(f"Error occurred while initializing database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
