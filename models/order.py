import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, select, text
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from settings.database import Base, connection


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
from app.schemas.order import OrderCreate

class EquipmentOrder(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipments.id"))
    order_date: Mapped[datetime]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    status = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)

    # Relationships
    user = relationship("User", back_populates="equipment_orders")
    equipment = relationship("Equipment", back_populates="equipment_orders")

    @classmethod
    @connection
    def check_overlaping(cls, order_in: OrderCreate, session: Session = None):
        query = select(cls).filter(
            cls.equipment_id == order_in.equipment_id,
            cls.status != "cancelled",
            (
                (cls.start_time <= order_in.start_time)
                & (cls.end_time > order_in.start_time)
            )
            | (
                (cls.start_time < order_in.end_time)
                & (cls.end_time >= order_in.end_time)
            ),
        )
        rows = session.execute(query)
        return rows.scalar_one_or_none()


class Order(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipments.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.PENDING, server_default=text("'PENDING'")
    )
    total_price: Mapped[int]

    # Связи
    user = relationship("User", back_populates="orders")
    equipment = relationship("Equipment", back_populates="orders")
