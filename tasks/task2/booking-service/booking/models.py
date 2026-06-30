from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str]
    hotel_id: Mapped[str]
    promo_code: Mapped[Optional[str]]
    discount_percent: Mapped[float]
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"Booking(id={self.id!r}, user_id={self.user_id!r}, "
            f"hotel_id={self.hotel_id!r}, price={self.price!r})"
        )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
