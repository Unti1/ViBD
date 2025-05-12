from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from models.user import User, UserStatus
from models.work_shift import WorkShift

from app.schemas.shift import (
    WorkShift as WorkShiftSchema,
    WorkShiftCreate,
    WorkShiftUpdate,
    WorkShiftWithDetails,
)

router = APIRouter()


@router.get("/", response_model=List[WorkShiftWithDetails])
def read_shifts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список рабочих смен.
    """
    if current_user.role == UserStatus.ADMIN:
        shifts = WorkShift.get_all()
    elif current_user.role == UserStatus.TRAINER:
        shifts = WorkShift.get_all_by_creterias(trainer_id=current_user.id)
    else:
        shifts = WorkShift.get_all_by_creterias(is_available=True)
    return [
        WorkShiftWithDetails(**shift.__dict__, trainer_name=shift.trainer.full_name)
        for shift in shifts
    ]


@router.post("/", response_model=WorkShiftSchema)
def create_shift(
    *,
    shift_in: Annotated[WorkShiftCreate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создать новую рабочую смену.
    """
    if current_user.role not in [UserStatus.ADMIN, UserStatus.TRAINER]:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для создания смены",
        )

    # Проверка на пересечение с другими сменами
    overlapping_shifts = WorkShift.check_overlaping(shift_in)

    if overlapping_shifts:
        raise HTTPException(
            status_code=400,
            detail="Выбранное время уже занято",
        )

    shift = WorkShift.create(**dict(shift_in))
    return shift


@router.get("/{shift_id}", response_model=WorkShiftWithDetails)
def read_shift(
    *,
    shift_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию о рабочей смене.
    """
    shift = WorkShift.get(id=shift_id)
    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Смена не найдена",
        )
    if current_user.role == "client" and not shift.is_available:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для просмотра смены",
        )
    return WorkShiftWithDetails(**shift.__dict__, trainer_name=shift.trainer.full_name)


@router.put("/{shift_id}", response_model=WorkShiftSchema)
def update_shift(
    *,
    shift_id: int,
    shift_in: Annotated[WorkShiftUpdate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить информацию о рабочей смене.
    """
    shift = WorkShift.get(id=shift_id)
    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Смена не найдена",
        )
    if current_user.role != UserStatus and shift.trainer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для обновления смены",
        )

    shift = WorkShift.update(shift_id, **dict(shift_in))
    return shift


@router.delete("/{shift_id}")
def delete_shift(
    *,
    shift_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Удалить рабочую смену.
    """
    shift = WorkShift.get(id=shift_id)
    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Смена не найдена",
        )
    if current_user.role != "admin" and shift.trainer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для удаления смены",
        )

    WorkShift.delete(shift_id)
    return {"message": "Смена успешно удалена"}
