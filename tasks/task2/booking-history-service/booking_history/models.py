from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BookingHistRec(Base):
    __tablename__ = "booking_hist_rec"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_id: Mapped[int]
    user_id: Mapped[str]
    hotel_id: Mapped[str]
    price: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return (
            f"BookingHistRec(id={self.id!r}, booking_id={self.booking_id!r}, "
            f"user_id={self.user_id}, hotel_id={self.hotel_id}"
        )
