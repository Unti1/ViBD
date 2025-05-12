from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.api import deps
from app.core.security import get_password_hash
from models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список пользователей.
    """
    users = User.get_all()
    return users


@router.post("/", response_model=UserSchema)
def create_user(
    *,
    user_in: Annotated[UserCreate, Depends()],
) -> Any:
    """
    Создать нового пользователя.
    """
    user = User.get(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует.",
        )
    user = User.create(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role,
    )

    return user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    user_in: Annotated[UserUpdate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить текущего пользователя.
    """
    user_data = jsonable_encoder(current_user)
    update_data = dict(user_in)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    User.update(user_data.id, **update_data)
    return current_user


@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить текущего пользователя.
    """
    return current_user
