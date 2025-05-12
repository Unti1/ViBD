from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.core.security import ALGORITHM
from app.schemas.token import TokenPayload
from models.user import User
from settings.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)


def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не удалось проверить учетные данные",
        )
    user = User.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=400, detail="Пользователь не имеет прав администратора"
        )
    return current_user


def get_current_trainer_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "trainer":
        raise HTTPException(status_code=400, detail="Пользователь не является тренером")
    return current_user
