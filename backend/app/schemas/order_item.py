"""Pydantic schemas for the OrderItem entity."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderItemBase(BaseModel):
    """Shared fields for OrderItem schemas."""

    product_name: str
    quantity: int
    price: Decimal


class OrderItemCreate(OrderItemBase):
    """Schema for creating a new OrderItem (used when creating an Order)."""

    pass


class OrderItemRead(OrderItemBase):
    """Schema for returning an OrderItem in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
