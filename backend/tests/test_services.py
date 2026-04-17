"""Unit tests for services."""

from datetime import date
from app.models.enums import OrderStatus
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.order_service import OrderService
from app.models.customer import Customer

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
            OrderItemCreate(product_name="Product A", quantity=2, price=10.50),
            OrderItemCreate(product_name="Product B", quantity=1, price=5.00),
        ]
    )
    
    order = service.create_order(order_data)
    
    # 2 * 10.50 + 1 * 5.00 = 21.00 + 5.00 = 26.00
    assert order.total == 26.00
