from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Numeric
from datetime import datetime
from decimal import Decimal
from .base import Base

class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None] 
    start_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    seller_id: Mapped[int] 
    status: Mapped[str] = mapped_column(default="active", server_default="active") 
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    winner_id: Mapped[int | None] 
    final_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))