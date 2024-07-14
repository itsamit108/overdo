from fastapi import HTTPException
from fastapi import status

from schemas import UserRead


def check_user_authorization(user_id: int, current_user: UserRead):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user",
        )
