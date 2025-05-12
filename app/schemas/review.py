from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    equipment_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewInDBBase(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Review(ReviewInDBBase):
    pass


class ReviewWithDetails(Review):
    equipment_name: str
    user_name: str 