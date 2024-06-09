from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Todo, User
from schemas import TodoCreate, UserRead


def check_user_authorization(user_id: int, current_user: UserRead):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user",
        )


def create_todo(
    user_id: int,
    req: TodoCreate,
    current_user: UserRead,
    session: Session = Depends(get_session),
):
    check_user_authorization(user_id, current_user)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    todo = Todo(title=req.title, description=req.description, user_id=user_id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def get_todo(
    user_id: int,
    todo_id: int,
    current_user: UserRead,
    session: Session = Depends(get_session),
):
    check_user_authorization(user_id, current_user)
    todo = session.exec(
        select(Todo).where(Todo.todo_id == todo_id, Todo.user_id == user_id)
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


def update_todo(
    user_id: int,
    todo_id: int,
    req: TodoCreate,
    current_user: UserRead,
    session: Session = Depends(get_session),
):
    check_user_authorization(user_id, current_user)
    todo = session.exec(
        select(Todo).where(Todo.todo_id == todo_id, Todo.user_id == user_id)
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    # Update the todo's attributes
    for key, value in req.dict().items():
        setattr(todo, key, value)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(
    user_id: int,
    todo_id: int,
    current_user: UserRead,
    session: Session = Depends(get_session),
):
    check_user_authorization(user_id, current_user)
    todo = session.exec(
        select(Todo).where(Todo.todo_id == todo_id, Todo.user_id == user_id)
    ).first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    session.delete(todo)
    session.commit()
    return todo


def get_todos_for_user(
    user_id: int,
    current_user: UserRead,
    session: Session = Depends(get_session),
):
    check_user_authorization(user_id, current_user)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    todos = session.exec(select(Todo).where(Todo.user_id == user_id)).all()
    return todos
