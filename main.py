from fastapi import FastAPI, APIRouter
from sqlmodel import SQLModel
from database import engine
from routers import auth, users, todos

SQLModel.metadata.create_all(engine)

app = FastAPI()
router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
