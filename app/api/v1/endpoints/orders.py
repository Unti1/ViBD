from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from models.user import User, UserStatus
from models.order import EquipmentOrder, Order
from models.equipment import Equipment
from app.schemas.order import (
    Order as OrderSchema,
    OrderCreate,
    OrderUpdate,
    OrderWithDetails,
)

router = APIRouter()


@router.get("/", response_model=List[OrderWithDetails])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить список заказов.
    """
    if current_user.role == UserStatus.ADMIN:
        orders: list[Order] = EquipmentOrder.get_all()
    elif current_user.role == UserStatus.TRAINER:
        orders: list[Order] = EquipmentOrder.get_all(user_id = current_user.id)
    else:
        orders: list[Order] = EquipmentOrder.get_all(EquipmentOrder.user_id == current_user.id)
    
    return [
        OrderWithDetails(
            **order.__dict__,
            equipment_name=order.equipment.name,
            user_name=order.user.full_name
        )
        for order in orders
    ]


@router.post("/", response_model=OrderSchema)
def create_order(
    *,
    order_in: Annotated[OrderCreate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Создать новый заказ.
    """
    equipment = Equipment.get(id = order_in.equipment_id)
    if not equipment:
        raise HTTPException(
            status_code=404,
            detail="Оборудование не найдено",
        )
    if not equipment.is_available:
        raise HTTPException(
            status_code=400,
            detail="Оборудование недоступно",
        )
    
    # Проверка на пересечение с другими заказами
    overlapping_orders = EquipmentOrder.check_overlaping(order_in)
    
    if overlapping_orders:
        raise HTTPException(
            status_code=400,
            detail="Выбранное время уже занято",
        )
    
    order = EquipmentOrder.create(
        **dict(order_in),
        user_id=current_user.id
    )
    return order


@router.get("/{order_id}", response_model=OrderWithDetails)
def read_order(
    *,
    order_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию о заказе.
    """
    order = EquipmentOrder.get(id = order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Заказ не найден",
        )
    if current_user.role != UserStatus.ADMIN and order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для просмотра заказа",
        )
    return OrderWithDetails(
        **order.__dict__,
        equipment_name=order.equipment.name,
        user_name=order.user.full_name
    )


@router.put("/{order_id}", response_model=OrderSchema)
def update_order(
    *,
    order_id: int,
    order_in: Annotated[OrderUpdate, Depends()],
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Обновить статус заказа.
    """
    order = EquipmentOrder.get(id = order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Заказ не найден",
        )
    if current_user.role != UserStatus.ADMIN and order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для обновления заказа",
        )
    EquipmentOrder.update(id=order_id, **dict(order_in))
    return order 