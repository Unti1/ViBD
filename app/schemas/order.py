from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from models.order import OrderStatus


class OrderBase(BaseModel):
    equipment_id: int
    start_time: datetime
    end_time: datetime
    status: OrderStatus = OrderStatus.PENDING


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class OrderInDBBase(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Order(OrderInDBBase):
    pass


class OrderWithDetails(Order):
    equipment_name: str
    user_name: str