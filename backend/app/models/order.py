"""Order ORM model."""

import datetime
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import OrderStatus


class Order(Base):
    """Represents a customer order."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=OrderStatus.PENDING.value,
    )
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    # Relationships
    customer: Mapped["Customer"] = relationship(  # noqa: F821
        back_populates="orders",
    )
    items: Mapped[list["OrderItem"]] = relationship(  # noqa: F821
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} status={self.status}>"
