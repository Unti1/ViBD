from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class EquipmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    condition: str
    is_available: bool = True
    purchase_date: datetime


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    condition: Optional[str] = None
    is_available: Optional[bool] = None
    last_maintenance_date: Optional[datetime] = None


class EquipmentInDBBase(EquipmentBase):
    id: int
    last_maintenance_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Equipment(EquipmentInDBBase):
    pass


class MaintenanceRecordBase(BaseModel):
    equipment_id: int
    maintenance_date: datetime
    description: str
    cost: Optional[float] = None
    performed_by: str


class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass


class MaintenanceRecord(MaintenanceRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True