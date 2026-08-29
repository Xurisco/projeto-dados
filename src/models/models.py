from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class Customer(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2)
    email: EmailStr
    city: str
    state: str = Field(..., min_length=2, max_length=2)
    created_at: str

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return value.strip().title()


class Product(BaseModel):
    id: int = Field(..., gt=0)
    sku: str
    name: str
    category: str
    subcategory: str
    brand: str
    cost_price: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    rating: float = Field(..., ge=1.0, le=5.0)

    @field_validator("name", "category", "subcategory", "brand")
    @classmethod
    def clean_strings(cls, value: str) -> str:
        return value.strip()


class Order(BaseModel):
    id: int = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    cost_price: float = Field(..., gt=0)
    shipping_cost: float = Field(..., ge=0)
    discount: float = Field(..., ge=0)
    payment_method: str
    status: str
    created_at: str