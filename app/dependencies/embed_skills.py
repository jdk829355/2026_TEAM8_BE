import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.dependencies.database import SessionLocal
from app.services.ai_service import AiService

service = AiService()
logger = logging.getLogger(__name__)

def embed_skills():
    db: Session = SessionLocal()
    try:
        skills_without_embedding = db.execute(text("""
            SELECT id, name FROM "SKILL" WHERE name_embedding IS NULL;
        """)).fetchall()

        if not skills_without_embedding:
            logger.info("name_embedding이 NULL인 SKILL 데이터가 없습니다. 임베딩 작업을 건너뜁니다.")
            return

        logger.info("임베딩 대상 SKILL 개수: %d", len(skills_without_embedding))
        skills = (i[1] for i in skills_without_embedding)

        embeddings = [service.encode_skill_name(skill) for skill in skills]
        for (skill_id, _), embedding in zip(skills_without_embedding, embeddings):
            db.execute(text("""
                UPDATE "SKILL" SET name_embedding = :embedding WHERE id = :skill_id;
            """), {"embedding": embedding, "skill_id": skill_id})

        db.commit()
        logger.info("SKILL 임베딩 업데이트를 DB에 커밋했습니다.")
    finally:
        db.close()


if __name__ == "__main__":
    embed_skills()