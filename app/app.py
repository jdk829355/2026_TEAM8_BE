from fastapi import FastAPI
from app.routers.skill.skill_router import router as skill_router

app = FastAPI()

app.include_router(skill_router)

@app.get("/")
def read_root():
    return "Hello from trithon-team8-be!"