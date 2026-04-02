import json
import os
from collections import defaultdict

from llm.extractor import extract_assignments
from utils.validator import validate_assignments


BASE_DIR = os.path.dirname(__file__)


def run(*, conversation, users):

    # 3. participants → 유저 정보로 변환
    participants = {
        uid: users[uid]
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
    result = validate_assignments(result, conversation["participants"])

    if result.get("error"):
        print("=== FINAL RESULT ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return []
    
    return result["assignments"]
