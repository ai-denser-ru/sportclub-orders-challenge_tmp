"""Service layer for Order business logic."""

from datetime import date

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.models.enums import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.customer_repository import CustomerRepository
from app.schemas.order import OrderCreate, OrderStatusUpdate


class OrderService:
    """Coordinates business rules for Orders."""

    def __init__(self, db: Session) -> None:
        self.order_repo = OrderRepository(db)
        self.customer_repo = CustomerRepository(db)

    def list_orders(
        self,
        status: OrderStatus | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[Order]:
        """Return filtered list of orders."""
        return self.order_repo.get_all(
            status=status,
            date_from=date_from,
            date_to=date_to,
        )

    def get_order(self, order_id: int) -> Order:
        """Return a single order or raise NotFoundError."""
        order = self.order_repo.get_by_id(order_id)
        if order is None:
            raise NotFoundError("Order", order_id)
        return order

    def create_order(self, data: OrderCreate) -> Order:
        """Create a new order with items and compute total."""
        # Validate customer exists
        customer = self.customer_repo.get_by_id(data.customer_id)
        if customer is None:
            raise NotFoundError("Customer", data.customer_id)

        if not data.items:
            raise ValidationError("Order must contain at least one item")

        # Build order items
        items = [
            OrderItem(
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
            )
            for item in data.items
        ]

        # Compute total from items
        total = sum(item.quantity * item.price for item in data.items)

        order = Order(
            customer_id=data.customer_id,
            date=data.date,
            status=data.status.value,
            total=round(total, 2),
            items=items,
        )

        return self.order_repo.create(order)

    def update_status(self, order_id: int, data: OrderStatusUpdate) -> Order:
        """Update order status after validation."""
        order = self.get_order(order_id)  # raises NotFoundError if missing

        if order.status == data.status.value:
            raise ValidationError(
                f"Order is already in {data.status.value} status"
            )

        return self.order_repo.update_status(order, data.status)
