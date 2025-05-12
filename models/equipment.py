from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from settings.database import Base


class Equipment(Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    equipmentorders_id: Mapped[int] = mapped_column(ForeignKey('equipmentorders.id'))
    description: Mapped[str] = mapped_column(String(1000))
    category: Mapped[str] = mapped_column(String(100))
    condition: Mapped[str] = mapped_column(String(50), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    purchase_date: Mapped[datetime]
    last_maintenance_date: Mapped[datetime]
    quantity: Mapped[int]
    price_per_hour: Mapped[float]

    # Relationships
    equipment_orders = relationship("EquipmentOrder", back_populates="equipments")
    # orders = relationship("Order", back_populates="equipment")
    maintenance_records = relationship("MaintenanceRecord", back_populates="equipment")
    reviews = relationship("Review", back_populates="equipment")


class MaintenanceRecord(Base):
    equipment_id = mapped_column(Integer, ForeignKey("equipments.id"), nullable=False)
    maintenance_date: Mapped[datetime]
    description = mapped_column(String(1000), nullable=False)
    cost: Mapped[float]
    performed_by: Mapped[str] = mapped_column(String(255))

    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_records")
