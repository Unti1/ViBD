from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class WorkShiftBase(BaseModel):
    trainer_id: int
    start_time: datetime
    end_time: datetime
    is_available: bool = True


class WorkShiftCreate(WorkShiftBase):
    pass


class WorkShiftUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_available: Optional[bool] = None


class WorkShiftInDBBase(WorkShiftBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkShift(WorkShiftInDBBase):
    pass


class WorkShiftWithDetails(WorkShift):
    trainer_name: str 
    