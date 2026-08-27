import random
from datetime import datetime

from src.models.models import Order, Product


ORDER_STATUSES = [
    "pending",
    "paid",
    "shipped",
    "delivered",
    "cancelled",
]


def generate_order(
    order_id: int,
    customer_ids: list[int],
    products: list[Product],
) -> Order:
    product = random.choice(products)

    return Order(
        id=order_id,
        customer_id=random.choice(customer_ids),
        product_id=product.id,
        quantity=random.randint(1, 5),
        unit_price=product.price,
        order_date=datetime.now(),
        status=random.choice(ORDER_STATUSES),
    )