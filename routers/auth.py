from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from database import get_session
from schemas import Token, UserCreate
from services.auth import login_for_access_token, register_for_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    req: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    return login_for_access_token(req, session)


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(req: UserCreate, session: Session = Depends(get_session)):
    return register_for_access_token(req, session)
