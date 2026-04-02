import json
import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(__file__)

load_dotenv(os.path.join(BASE_DIR, "../../../.env.secret"))

from app.dependencies.ai.llm.extractor import extract_assignments
from app.dependencies.ai.utils.validator import validate_assignments






def run(*, conversation, users) -> list[dict]:

    # 3. participants → 유저 정보로 변환
    participants = {
        str(uid): users[str(uid)]
        for uid in conversation["participants"]
    }

    conversation["participants"] = participants

    # 4. LLM 실행
    result = extract_assignments(conversation)

    if result.get("error"):
        print("=== FINAL RESULT ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return []

    # 5. validator 적용
    result = validate_assignments(result, conversation["participants"], users)

    if result.get("error"):
        print("=== FINAL RESULT ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return []
    
    return result["assignments"] # type: ignore

if __name__ == "__main__":
    conversation = {
        "participants": ["user1", "user2"],
        "messages": [
            {"sender": "user1", "text": "나는 자바를 가르쳐줄 수 있어. 자바는 객체지향 언어야."},
            {"sender": "user2", "text": "나는 자바를 배우고 싶어. 자바는 어렵다고 들었어."},
        ]
    }
    users = {
        "user1": {"name": "Alice", "teach_subjects": ["Java"], "learn_subjects": ["Python"], "level": "intermediate"},
        "user2": {"name": "Bob", "teach_subjects": ["Python"], "learn_subjects": ["Java"], "level": "beginner"},
    }

    r = run(
        conversation=conversation,
        users=users
    )

    print("=== TODO ASSIGNMENTS ===")
    print(json.dumps(r, indent=2, ensure_ascii=False))
