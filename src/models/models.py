from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class Customer(BaseModel):
    id: int
    name: str
    email: EmailStr
    birth_date: date
    city: str
    state: str


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class Order(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    order_date: datetime
    status: str