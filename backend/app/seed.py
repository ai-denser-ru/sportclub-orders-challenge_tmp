"""Database seed script – populates the DB with initial data.

Run with: uv run python -m app.seed
"""

import random
from datetime import date, timedelta

from app.core.database import Base, SessionLocal, engine
from app.models.customer import Customer
from app.models.enums import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem

# ---------------------------------------------------------------------------
# Seed Data Constants
# ---------------------------------------------------------------------------

CUSTOMERS = [
    {"name": "María García", "email": "maria.garcia@example.com"},
    {"name": "Carlos López", "email": "carlos.lopez@example.com"},
    {"name": "Ana Martínez", "email": "ana.martinez@example.com"},
    {"name": "Pedro Rodríguez", "email": "pedro.rodriguez@example.com"},
    {"name": "Laura Fernández", "email": "laura.fernandez@example.com"},
]

PRODUCTS = [
    ("Camiseta Oficial Home", 89.99),
    ("Camiseta Oficial Away", 84.99),
    ("Short de Entrenamiento", 45.50),
    ("Medias Oficiales", 15.00),
    ("Balón de Fútbol Pro", 120.00),
    ("Guantes de Portero", 65.00),
    ("Chaqueta de Invierno", 130.00),
    ("Gorra del Club", 25.00),
    ("Bufanda Oficial", 20.00),
    ("Mochila Deportiva", 55.00),
    ("Botella Térmica", 18.50),
    ("Sudadera con Capucha", 75.00),
    ("Polo de Viaje", 60.00),
    ("Pantalón de Chándal", 50.00),
    ("Toalla del Club", 30.00),
]

STATUSES = [OrderStatus.PENDING, OrderStatus.PAID, OrderStatus.CANCELLED]

# ---------------------------------------------------------------------------
# Seed Logic
# ---------------------------------------------------------------------------


def seed() -> None:
    """Create tables and populate with seed data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Customer).count() > 0:
            print("⚠️  Database already seeded. Skipping.")
            return

        # 1. Create Customers
        customers: list[Customer] = []
        for c in CUSTOMERS:
            customer = Customer(name=c["name"], email=c["email"])
            db.add(customer)
            customers.append(customer)
        db.flush()  # assign IDs
        print(f"✅ Created {len(customers)} customers")

        # 2. Create 20 Orders with 50 Items total
        orders: list[Order] = []
        total_items = 0
        target_orders = 20
        target_items = 50

        # Pre-calculate items per order to hit exactly 50
        # Distribute ~2-3 items per order, ensuring total = 50
        items_per_order: list[int] = []
        remaining_items = target_items
        for i in range(target_orders):
            orders_left = target_orders - i
            if orders_left == 1:
                count = remaining_items
            else:
                avg = remaining_items / orders_left
                count = max(1, min(5, random.randint(int(avg) - 1, int(avg) + 1)))
                count = min(count, remaining_items - (orders_left - 1))
            items_per_order.append(count)
            remaining_items -= count

        random.seed(42)  # Reproducible seed data

        for i in range(target_orders):
            customer = random.choice(customers)
            order_date = date(2025, 1, 1) + timedelta(days=random.randint(0, 365))
            status = random.choice(STATUSES)

            order = Order(
                customer_id=customer.id,
                date=order_date,
                status=status.value,
                total=0,
            )
            db.add(order)
            db.flush()

            # Create items for this order
            order_total = 0.0
            num_items = items_per_order[i]
            selected_products = random.sample(
                PRODUCTS, min(num_items, len(PRODUCTS))
            )

            for product_name, base_price in selected_products[:num_items]:
                qty = random.randint(1, 4)
                item = OrderItem(
                    order_id=order.id,
                    product_name=product_name,
                    quantity=qty,
                    price=base_price,
                )
                db.add(item)
                order_total += qty * base_price
                total_items += 1

            order.total = round(order_total, 2)
            orders.append(order)

        db.commit()
        print(f"✅ Created {len(orders)} orders")
        print(f"✅ Created {total_items} order items")
        print("🎉 Database seeding complete!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
