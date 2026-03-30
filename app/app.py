from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.routers.announcement.announcement_router import router as announcement_router
from app.routers.auth.auth_router import router as auth_router
from app.routers.chat.chat_router import router as chat_router
from app.routers.matching.matching_router import router as matching_router
from app.routers.skill.skill_router import router as skill_router
from app.routers.todo.todo_router import router as todo_router
from app.routers.user.user_router import router as user_router
from app.dependencies.database import engine
from app.models.base import Base
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown
    engine.dispose()


app = FastAPI(lifespan=lifespan, root_path="/api")

app.include_router(announcement_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(matching_router)
app.include_router(skill_router)
app.include_router(todo_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return "Hello from trithon-team8-be!"