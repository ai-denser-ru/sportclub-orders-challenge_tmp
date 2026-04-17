"""Pydantic schemas for the Customer entity."""

from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerBase(BaseModel):
    """Shared fields for Customer schemas."""

    name: str
    email: str


class CustomerCreate(CustomerBase):
    """Schema for creating a new Customer."""

    pass


class CustomerRead(CustomerBase):
    """Schema for returning a Customer in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
