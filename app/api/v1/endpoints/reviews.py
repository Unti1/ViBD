from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from models.user import User
from models.review import Review
from models.equipment import Equipment
from app.schemas.review import (
    Review as ReviewSchema,
    ReviewCreate,
    ReviewUpdate,
    ReviewWithDetails,
)

router = APIRouter()


@router.get("/", response_model=List[ReviewWithDetails])
def read_reviews(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список отзывов.
    """
    reviews = Review.get_all()
    return [
        ReviewWithDetails(
            **review.__dict__,
            equipment_name=review.equipment.name,
            user_name=review.user.full_name
        )
        for review in reviews
    ]


@router.post("/", response_model=ReviewSchema)
def create_review(
    *,
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создать новый отзыв.
    """
    equipment = Equipment.get(id = review_in.equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=404,
            detail="Оборудование не найдено",
        )
    
    # Проверка, оставлял ли пользователь уже отзыв на это оборудование
    existing_review = Review.get(
        equipment_id = review_in.equipment_id,
        user_id = current_user.id
    )
    
    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="Вы уже оставили отзыв на это оборудование",
        )
    
    review = Review.create(
        user_id=current_user.id,
        **dict(review_in)
    )
    return review


@router.get("/{review_id}", response_model=ReviewWithDetails)
def read_review(
    *,
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию об отзыве.
    """
    review = Review.get(id = review_id)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Отзыв не найден",
        )
    return ReviewWithDetails(
        **review.__dict__,
        equipment_name=review.equipment.name,
        user_name=review.user.full_name
    )


@router.put("/{review_id}", response_model=ReviewSchema)
def update_review(
    *,
    review_id: int,
    review_in: Annotated[ReviewUpdate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить отзыв.
    """
    review = Review.get(id = review_id)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Отзыв не найден",
        )
    if current_user.role != "admin" and review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для обновления отзыва",
        )
    Review.update(review_id, **dict(review_in))
    return review


@router.delete("/{review_id}")
def delete_review(
    *,
    review_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Удалить отзыв.
    """
    review = Review.get(id = review_id)
    if not review:
        raise HTTPException(
            status_code=404,
            detail="Отзыв не найден",
        )
    if current_user.role != "admin" and review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для удаления отзыва",
        )
    Review.delete(review_id)
    return {"message": "Отзыв успешно удален"} 