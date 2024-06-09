from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from schemas import TodoCreate, TodoRead, UserRead
from services import todos
from typing import List
from utils.oauth2 import get_current_user

router = APIRouter(prefix="/users/{user_id}", tags=["Todos"])


@router.post("/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create(
    user_id: int,
    req: TodoCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return todos.create_todo(user_id, req, current_user, session)


@router.get("/todos/{todo_id}", response_model=TodoRead, status_code=status.HTTP_200_OK)
async def read(
    user_id: int,
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return todos.get_todo(user_id, todo_id, current_user, session)


@router.put("/todos/{todo_id}", response_model=TodoRead, status_code=status.HTTP_200_OK)
async def update(
    user_id: int,
    todo_id: int,
    req: TodoCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return todos.update_todo(user_id, todo_id, req, current_user, session)


@router.delete(
    "/todos/{todo_id}", response_model=TodoRead, status_code=status.HTTP_200_OK
)
async def delete(
    user_id: int,
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return todos.delete_todo(user_id, todo_id, current_user, session)


@router.get("/todos", response_model=List[TodoRead], status_code=status.HTTP_200_OK)
async def read_todos_for_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return todos.get_todos_for_user(user_id, current_user, session)
