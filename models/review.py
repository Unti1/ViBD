from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings.database import Base


class Review(Base):
    user_id: Mapped[int] = mapped_column( ForeignKey("users.id"))
    equipment_id: Mapped[int] = mapped_column( ForeignKey("equipments.id"))
    rating: Mapped[int]
    comment: Mapped[str]

    user = relationship("User", back_populates="reviews")
    equipment = relationship("Equipment", back_populates="reviews") 