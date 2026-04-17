"""Repository for Customer data access."""

from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    """Encapsulates all database queries for Customers."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, customer_id: int) -> Customer | None:
        """Return a single customer by primary key."""
        return self.db.get(Customer, customer_id)

    def get_all(self) -> list[Customer]:
        """Return all customers."""
        return list(self.db.query(Customer).all())

    def create(self, customer: Customer) -> Customer:
        """Persist a new customer."""
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
