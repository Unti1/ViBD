from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.api import deps
from settings.config import settings
from app.core.security import create_access_token, verify_password
from models.user import User

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Получить OAuth2 совместимый токен для аутентификации.
    """
    user = User.get(email = form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Неверный email или пароль",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Неактивный пользователь",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token")
def test_token(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    Проверить токен доступа.
    """
    return current_user 