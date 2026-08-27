from src.generators.customer_generator import generate_customer
from src.generators.product_generator import generate_product
from src.generators.order_generator import generate_order
from src.models.models import Customer, Product, Order


def test_generate_customer():
    customer = generate_customer(1)

    assert isinstance(customer, Customer)
    assert customer.id == 1


def test_generate_product():
    product = generate_product(1)

    assert isinstance(product, Product)
    assert product.id == 1
    assert product.price > 0
    assert product.stock >= 0


def test_generate_order():
    products = [generate_product(1), generate_product(2)]
    order = generate_order(1, [1, 2, 3], products)

    assert isinstance(order, Order)
    assert order.id == 1
    assert order.quantity > 0