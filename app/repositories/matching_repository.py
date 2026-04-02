from datetime import datetime
from typing import Any
from uuid import UUID
from app.models import User

from sqlalchemy.orm import Session, aliased

from app.models.announcement_models import Announcement
from app.models.chat_models import Chatroom, MatchingRequest
from app.models.matching_models import Matching, Teach
from app.models.skill_models import Skill

from app.core.verify_jwt import get_current_user_id


class MatchingRepository:
    def accept_matching_request(
        self,
        db: Session,
        matching_request_id: UUID,
        matching_id: UUID,
    ) -> Chatroom | None:
        """이미 있는 matching에 대해 matching request를 연결하고 matching request를 삭제하는 로직"

        Args:
            db (Session):
            matching_request_id (UUID):
            matching_id (UUID):

        Returns:
            Chatroom | None:
        """
        matching_request = (
            db.query(MatchingRequest)
            .filter(MatchingRequest.id == matching_request_id)
            .first()
        )
        if matching_request is None:
            return None

        chatroom = (
            db.query(Chatroom).filter(Chatroom.id == matching_request.room_id).first()
        )
        if chatroom is None:
            return None

        chatroom.matching_id = matching_id  # type: ignore
        db.delete(matching_request)
        db.commit()
        db.refresh(chatroom)
        return chatroom

    def create_matching(
        self, db: Session, announcement_id: UUID, host_id: UUID, guest_id: UUID
    ) -> Matching | None:

        announcement = (
            db.query(Announcement).filter(Announcement.id == announcement_id).first()
        )
        if announcement is None:
            return None

        # 생성 이름: 이름 없는 매칭 YYYYMMDD
        name = f"이름 없는 매칭 {datetime.now().strftime('%Y%m%d')}"

        matching = Matching(name=name)
        db.add(matching)
        db.commit()
        db.refresh(matching)

        teach: set[Teach] = {
            Teach(
                teacher_id=announcement.user_id,
                skill_id=announcement.can_teach_skill,
                matching_id=matching.id,
                status="ACTIVE",
            ),
            Teach(
                teacher_id=guest_id,
                skill_id=announcement.want_to_skill,
                matching_id=matching.id,
                status="ACTIVE",
            ),
        }
        for t in teach:
            db.add(t)
        db.commit()
        return matching

    def create_matching_from_request(
        self,
        db: Session,
        matching_request_id: UUID,
    ) -> tuple[UUID, UUID, UUID, UUID] | None:
        matching_request = (
            db.query(MatchingRequest)
            .filter(MatchingRequest.id == matching_request_id)
            .first()
        )
        if matching_request is None:
            return None

        chatroom = (
            db.query(Chatroom).filter(Chatroom.id == matching_request.room_id).first()
        )
        if chatroom is None:
            return None

        announcement = (
            db.query(Announcement)
            .filter(Announcement.id == chatroom.announcement_id)
            .first()
        )
        if announcement is None or announcement.user_id is None:
            return None

        host_user_id = announcement.user_id
        guest_user_id = (
            matching_request.from_user_id
            if matching_request.from_user_id != host_user_id # type: ignore
            else matching_request.to_user_id
        )
        if guest_user_id is None:
            return None

        try:
            name = f"이름 없는 매칭 {datetime.now().strftime('%Y%m%d')}"
            matching = Matching(name=name)
            db.add(matching)
            db.flush()

            db.add(
                Teach(
                    teacher_id=host_user_id,
                    skill_id=announcement.can_teach_skill,
                    matching_id=matching.id,
                    status="ACTIVE",
                )
            )
            db.add(
                Teach(
                    teacher_id=guest_user_id,
                    skill_id=announcement.want_to_skill,
                    matching_id=matching.id,
                    status="ACTIVE",
                )
            )

            chatroom.matching_id = matching.id  # type: ignore
            db.delete(matching_request)
            db.commit()
        except Exception:
            db.rollback()
            raise

        return (matching.id, host_user_id, guest_user_id, announcement.id)  # type: ignore

    def matching_request_info(self, db: Session, matching_request_id: UUID) -> dict[str, Any] | None:
        matching_request = (
            db.query(MatchingRequest)
            .filter(MatchingRequest.id == matching_request_id)
            .first()
        )
        if matching_request is None:
            return None

        chatroom = (
            db.query(Chatroom).filter(Chatroom.id == matching_request.room_id).first()
        )
        if chatroom is None:
            return None

        announcement = (
            db.query(Announcement)
            .filter(Announcement.id == chatroom.announcement_id)
            .first()
        )
        if announcement is None or announcement.user_id is None:
            return None

        host_user_id = announcement.user_id
        guest_user_id = (
            matching_request.from_user_id
            if matching_request.from_user_id != host_user_id  # type: ignore
            else matching_request.to_user_id
        )
        if guest_user_id is None:
            return None
        return {"host_user_id": host_user_id, "guest_user_id": guest_user_id}

    def reject_matching_request(self, db: Session, matching_request_id: UUID) -> bool:
        matching_request = (
            db.query(MatchingRequest)
            .filter(MatchingRequest.id == matching_request_id)
            .first()
        )
        if matching_request is None:
            return False

        db.delete(matching_request)
        db.commit()
        return True

    def get_matching_request(self, db: Session, user_id: UUID) -> tuple[list[tuple[MatchingRequest, str]], list[tuple[MatchingRequest, str]]]:


        matching_request_send = (
            db.query(MatchingRequest, User.name.label("opponent_name"))
            .filter(MatchingRequest.from_user_id == user_id)
            .join(User, User.id == MatchingRequest.to_user_id)
            .all()
        )
        matching_reqeust_receive = (
            db.query(MatchingRequest, User.name.label("opponent_name"))
            .filter(MatchingRequest.to_user_id == user_id)
            .join(User, User.id == MatchingRequest.from_user_id)
            .all()
        )
        return matching_request_send, matching_reqeust_receive
    
    def get_my_matchings(self, db: Session, user_id: UUID):
        # 내가 참여한(Teach 테이블에 내 ID가 있는) 매칭들을 찾고, 
        # 그 매칭의 이름과 내가 가르치는 스킬, 배우는 스킬을 가져옵니다.
        
        # 1. 내가 참여한 매칭 ID들 먼저 찾기
        my_matching_ids = db.query(Teach.matching_id).filter(Teach.teacher_id == user_id).subquery()

        # 2. 해당 매칭들의 정보와 스킬 정보를 조인해서 가져오기
        # (리스트용이므로 일단 간단하게 매칭 이름과 상태 정도만 가져오거나, 
        # 필요하다면 아래처럼 상세하게 조인합니다.)
        results = (
            db.query(
                Matching.id.label("matching_id"),
                Matching.name,
                Skill.name.label("skill_name")
            )
            .join(Teach, Teach.matching_id == Matching.id)
            .join(Skill, Skill.id == Teach.skill_id)
            .filter(Matching.id.in_(my_matching_ids))
            .filter(Teach.teacher_id == user_id) # 내가 가르치는 스킬 기준
            .all()
        )
        
        return results
    
    def get_by_id(self, db: Session, matching_id: UUID, current_user_id: UUID):
        # 1. 상대방 정보 (이름, ID, 상대방이 가르치는 스킬 이름)
        opponent_data = (
            db.query(User.name, User.id, Skill.name.label("skill_name"))
            .join(Teach, Teach.teacher_id == User.id)
            .join(Skill, Skill.id == Teach.skill_id)
            .filter(Teach.matching_id == matching_id)
            .filter(User.id != current_user_id) # 내가 아닌 상대방
            .first()
        )

        # 2. 내가 가르치는 스킬 정보
        my_skill_data = (
            db.query(Skill.name)
            .join(Teach, Teach.skill_id == Skill.id)
            .filter(Teach.matching_id == matching_id)
            .filter(Teach.teacher_id == current_user_id)
            .first()
        )

        if not opponent_data:
            return None

        # ⭐ 중요: DB 모델이 아니라, 라우터가 기대하는 형태의 '딕셔너리'나 '객체'로 반환합니다.
        return {
            "opponent_name": opponent_data.name,
            "opponent_id": str(opponent_data.id),
            "teaching_skill": my_skill_data.name if my_skill_data else "Unknown",
            "learning_skill": opponent_data.skill_name # 상대방이 가르치는 게 내가 배우는 것
        }
    
    def update_matching_and_teach(self, db: Session, matching_id: UUID, user_id: UUID, name: str, status: str):
        # 1. MATCHING 테이블 존재 확인 및 이름 업데이트
        matching = db.query(Matching).filter(Matching.id == matching_id).first()
        if not matching:
            return None
        matching.name = name

        # 2. 나의 TEACH 상태 업데이트
        my_teach = db.query(Teach).filter(
            Teach.matching_id == matching_id, 
            Teach.teacher_id == user_id
        ).first()
        if my_teach:
            my_teach.status = status

        db.flush() # 변경 사항 임시 반영 (조회를 위해)

        # 3. 해당 매칭의 모든 TEACH 상태 확인
        all_teaches = db.query(Teach).filter(Teach.matching_id == matching_id).all()
        # 모든 TEACH의 status가 'COMPLETED'인지 체크 (두 개의 TEACH가 모두 COMPLETED여야 함)
        is_all_completed = len(all_teaches) == 2 and all(t.status == "COMPLETED" for t in all_teaches)

        db.commit()
        return matching, is_all_completed