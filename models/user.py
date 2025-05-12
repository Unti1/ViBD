from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings.database import Base


class UserStatus(str, Enum):
    ADMIN = "admin"
    TRAINER = "trainer"
    CLIENT = "client"


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    full_name: Mapped[str]
    role: Mapped[UserStatus]
    is_active: Mapped[bool] = mapped_column(default=True)

    # Связи
    orders = relationship("Order", back_populates="user")
    equipment_orders = relationship('EquipmentOrder', back_populates='user')
    reviews = relationship("Review", back_populates="user")
    sent_messages = relationship(
        "ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender"
    )
    received_messages = relationship(
        "ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver"
    )
    work_shifts = relationship("WorkShift", back_populates="trainer")


