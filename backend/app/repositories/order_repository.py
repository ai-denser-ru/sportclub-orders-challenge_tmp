"""Repository for Order data access."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.enums import OrderStatus
from app.models.order import Order


class OrderRepository:
    """Encapsulates all database queries for Orders."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        status: OrderStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Order]:
        """Return orders with optional filters on status and date range."""
        stmt = select(Order).options(joinedload(Order.customer))

        if status is not None:
            stmt = stmt.where(Order.status == status.value)
        if date_from is not None:
            stmt = stmt.where(Order.date >= date_from)
        if date_to is not None:
            stmt = stmt.where(Order.date <= date_to)

        stmt = stmt.order_by(Order.date.desc())
        return list(self.db.scalars(stmt).unique().all())

    def get_by_id(self, order_id: int) -> Order | None:
        """Return a single order by primary key with eager-loaded relations."""
        stmt = (
            select(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items),
            )
            .where(Order.id == order_id)
        )
        return self.db.scalars(stmt).unique().first()

    def create(self, order: Order) -> Order:
        """Persist a new order (with items cascaded)."""
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order: Order, new_status: OrderStatus) -> Order:
        """Update the status field of an existing order."""
        order.status = new_status.value
        self.db.commit()
        self.db.refresh(order)
        return order
