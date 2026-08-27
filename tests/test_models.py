from datetime import date

import pytest
from pydantic import ValidationError

from src.models.models import Customer, Product, Order


def test_customer():
    customer = Customer(
        id=1,
        name="Arthur",
        email="arthur@example.com",
        birth_date=date(2008, 1, 15),
        city="Londrina",
        state="PR",
    )

    assert customer.id == 1


def test_invalid_email():
    with pytest.raises(ValidationError):
        Customer(
            id=1,
            name="Arthur",
            email="email-invalido",
            birth_date=date(2008, 1, 15),
            city="Londrina",
            state="PR",
        )


def test_invalid_product_price():
    with pytest.raises(ValidationError):
        Product(
            id=1,
            name="Notebook",
            category="informatica",
            price=-100,
            stock=10,
        )


def test_invalid_order_quantity():
    with pytest.raises(ValidationError):
        Order(
            id=1,
            customer_id=1,
            product_id=1,
            quantity=0,
            unit_price=100,
            order_date="2026-08-27T15:30:00",
            status="paid",
        )