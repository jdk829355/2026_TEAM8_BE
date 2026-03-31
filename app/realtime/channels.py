def chat_room(room_id: str) -> str:
    return f"chat:room:{room_id}"

def user_event(user_id: str) -> str:
    return f"user:{user_id}:event"