def validate_assignments(result, participants, users):
    if result.get("error"):
        return result

    valid = []
    rejected = []

    def reject(assignment, reason):
        print(reason)
        rejected.append({
            "assignment": assignment,
            "reason": reason
        })

    value = [user for user in users.values()][0]
    allowed = set(value["teach_subjects"] + value["learn_subjects"])

    for a in result.get("assignments", []):

        subject = a.get("subject")

        # 🔥 디버깅 로그
        print("검증 중:", a)


        # 2️⃣ subject 검증
        if subject not in allowed:
            reject(a, f"subject 불일치: {subject} | allowed: {allowed}")
            continue

        if not a.get("task_name") or not a.get("task_info"):
            reject(a, "task_name/task_info 누락")
            continue

        difficulty = a.get("difficulty")
        if difficulty not in {"easy", "medium", "hard"}:
            reject(a, f"difficulty 값 오류: {difficulty}")
            continue

        valid.append(a)

    print("✅ 최종 valid 개수:", len(valid))
    print("🚫 최종 rejected 개수:", len(rejected))

    return {
        "assignments": valid,
        "rejected_assignments": rejected,
        "meta": {
            "llm_output_count": len(result.get("assignments", [])),
            "valid_count": len(valid),
            "rejected_count": len(rejected)
        }
    }
