"""Unit tests for services."""

from datetime import date
from decimal import Decimal

import pytest

from app.core.exceptions import ValidationError
from app.models.customer import Customer
from app.models.enums import OrderStatus
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.schemas.order_item import OrderItemCreate
from app.services.order_service import OrderService


def test_create_order_calculates_total_correctly(db_session):
    # Prepare dummy customer
    customer = Customer(id=1, name="John Doe", email="j@d.com")
    db_session.add(customer)
    db_session.commit()

    service = OrderService(db_session)

    order_data = OrderCreate(
        customer_id=1,
        date=date(2026, 4, 18),
        status=OrderStatus.PENDING,
        items=[
            OrderItemCreate(product_name="Product A", quantity=2, price=Decimal("10.50")),
            OrderItemCreate(product_name="Product B", quantity=1, price=Decimal("5.00")),
        ],
    )

    order = service.create_order(order_data)

    # 2 * 10.50 + 1 * 5.00 = 21.00 + 5.00 = 26.00
    assert order.total == Decimal("26.00")


def test_update_status_rejects_same_status(db_session):
    """A transition to the current status must raise ValidationError."""
    customer = Customer(id=1, name="Jane Doe", email="jane@d.com")
    db_session.add(customer)
    db_session.commit()

    service = OrderService(db_session)

    order_data = OrderCreate(
        customer_id=1,
        date=date(2026, 4, 18),
        status=OrderStatus.PENDING,
        items=[
            OrderItemCreate(product_name="Product A", quantity=1, price=Decimal("10.00")),
        ],
    )
    order = service.create_order(order_data)

    # Attempting PENDING → PENDING must fail
    with pytest.raises(ValidationError, match="already in PENDING status"):
        service.update_status(order.id, OrderStatusUpdate(status=OrderStatus.PENDING))
