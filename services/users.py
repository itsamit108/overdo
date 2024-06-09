from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import User
from schemas import UserCreate, UserRead
from utils.hash import Hash


def check_user_authorization(user_id: int, current_user: UserRead):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user",
        )


def get_user(
    user_id: int, current_user: UserRead, session: Session = Depends(get_session)
):
    check_user_authorization(user_id, current_user)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def update_user(
    user_id: int,
    req: UserCreate,
    current_user: UserRead,
    session: Session = Depends(get_session),
):
    check_user_authorization(user_id, current_user)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if the email already exists in another user
    if req.email != user.email:  # Check if email is being changed
        statement = select(User).where(User.email == req.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Update the user's attributes
    for key, value in req.model_dump().items():
        if key == "password":
            value = Hash.hash_password(value)  # Hash the password before updating
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(
    user_id: int, current_user: UserRead, session: Session = Depends(get_session)
):
    check_user_authorization(user_id, current_user)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return user
