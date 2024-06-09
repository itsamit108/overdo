from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from services import users
from schemas import UserCreate, UserRead
from utils.oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return users.get_user(user_id, current_user, session)


@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update(
    user_id: int,
    req: UserCreate,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return users.update_user(user_id, req, current_user, session)


@router.delete("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def delete(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    return users.delete_user(user_id, current_user, session)
