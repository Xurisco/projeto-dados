from datetime import datetime

from src.models.models import Customer, Product, Order
from src.transformers.data_transformer import (
    transform_customers,
    transform_products,
    transform_orders,
)


def test_transform_customer():
    customer = Customer(
        id=1,
        name=" Arthur ",
        email="arthur@example.com",
        birth_date="2008-01-15",
        city=" Londrina ",
        state="pr",
    )

    result = transform_customers([customer])[0]

    assert result.name == "Arthur"
    assert result.city == "Londrina"
    assert result.state == "PR"


def test_transform_product():
    product = Product(
        id=1,
        name=" Notebook ",
        category=" INFORMATICA ",
        price=3500,
        stock=10,
    )

    result = transform_products([product])[0]

    assert result.name == "Notebook"
    assert result.category == "informatica"


def test_transform_order():
    order = Order(
        id=1,
        customer_id=1,
        product_id=1,
        quantity=2,
        unit_price=100,
        order_date=datetime.now(),
        status="PAID",
    )

    result = transform_orders([order])[0]

    assert result.status == "paid"