from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.schemas.shift import WorkShiftCreate
from settings.database import Base, connection


class ShiftStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WorkShift(Base):
    trainer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    status: Mapped[str]
    is_available: Mapped[bool] = mapped_column(default=True)
    trainer = relationship("User", back_populates="work_shifts")

    @classmethod
    @connection
    def check_overlaping(cls, shift_in: WorkShiftCreate, session: Session = None):
        query = select(cls).filter(
            cls.trainer_id == shift_in.trainer_id,
            cls.is_available == True,
            (
                (cls.start_time <= shift_in.start_time)
                & (cls.end_time > shift_in.start_time)
            )
            | (
                (cls.start_time < shift_in.end_time)
                & (cls.end_time >= shift_in.end_time)
            ),
        )
        rows = session.execute(query)
        return rows.scalar_one_or_none()
