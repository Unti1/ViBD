from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from models.user import User
from models.equipment import Equipment, MaintenanceRecord
from app.schemas.equipment import (
    Equipment as EquipmentSchema,
    EquipmentCreate,
    EquipmentUpdate,
    MaintenanceRecord as MaintenanceRecordSchema,
    MaintenanceRecordCreate,
)

router = APIRouter()


@router.get("/", response_model=List[EquipmentSchema])
def read_equipment(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список оборудования.
    """
    equipment = Equipment.get_all()
    return equipment


@router.post("/", response_model=EquipmentSchema)
def create_equipment(
    *,
    equipment_in: Annotated[EquipmentCreate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создать новое оборудование.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для выполнения операции",
        )
    equipment = Equipment.create(**dict(equipment_in))
    return equipment


@router.get("/{equipment_id}", response_model=EquipmentSchema)
def read_equipment_by_id(
    equipment_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию об оборудовании по ID.
    """
    equipment = Equipment.get(id = equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=404,
            detail="Оборудование не найдено",
        )
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentSchema)
def update_equipment(
    *,
    equipment_id: int,
    equipment_in: Annotated[EquipmentUpdate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить информацию об оборудовании.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для выполнения операции",
        )
    equipment = Equipment.get(id = equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=404,
            detail="Оборудование не найдено",
        )
    Equipment.update(id=equipment.id, **dict(equipment_in))
    return equipment


@router.post("/{equipment_id}/maintenance", response_model=MaintenanceRecordSchema)
def create_maintenance_record(
    *,
    equipment_id: int,
    maintenance_in: Annotated[MaintenanceRecordCreate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создать запись об обслуживании оборудования.
    """
    if current_user.role not in ["admin", "trainer"]:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для выполнения операции",
        )
    equipment = Equipment.get(id = equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=404,
            detail="Оборудование не найдено",
        )
    maintenance = MaintenanceRecord.create(**dict(maintenance_in))
    equipment.last_maintenance_date = maintenance_in.maintenance_date
    # db.add(equipment)
    # db.commit()
    # db.refresh(maintenance)
    return maintenance 