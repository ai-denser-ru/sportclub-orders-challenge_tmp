"""Enum definitions for domain models."""

import enum


class OrderStatus(str, enum.Enum):
    """Allowed statuses for an Order."""

    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
