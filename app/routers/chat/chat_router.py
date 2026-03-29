from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/rooms")
def get_chat_rooms():
    return {"message": "get_chat_rooms handler"}


@router.post("/room")
def create_chat_room():
    return {"message": "create_chat_room handler"}


@router.websocket("/ws/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: str):
    _ = room_id
    await websocket.accept()
    await websocket.close()


@router.get("/room/{room_id}")
def get_chat_room(room_id: str):
    _ = room_id
    return {"message": "get_chat_room handler"}


@router.post("/room/{room_id}/ai-evaluate")
def evaluate_chat_room_ai(room_id: str):
    _ = room_id
    return {"message": "evaluate_chat_room_ai handler"}


@router.post("/exchange/{matching_request_id}")
def exchange_matching(matching_request_id: str):
    _ = matching_request_id
    return {"message": "exchange_matching handler"}
