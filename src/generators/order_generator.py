from datetime import datetime
import random
from src.models.models import Order, Product

PAYMENT_METHODS = ["Pix", "Cartão de Crédito", "Boleto", "Cartão de Débito"]
STATUS_OPTIONS = ["Concluído", "Concluído", "Concluído", "Concluído", "Cancelado", "Devolvido"]


def generate_order(
    order_id: int,
    customer_ids: list[int],
    products: list[Product],
) -> Order:
    product = random.choice(products)
    quantity = random.randint(1, 4)
    discount = round(random.uniform(0, 50.0), 2) if random.random() < 0.3 else 0.0
    shipping_cost = round(random.uniform(10.0, 45.0), 2)

    return Order(
        id=order_id,
        customer_id=random.choice(customer_ids),
        product_id=product.id,
        quantity=quantity,
        unit_price=product.price,
        cost_price=product.cost_price,
        shipping_cost=shipping_cost,
        discount=discount,
        payment_method=random.choice(PAYMENT_METHODS),
        status=random.choice(STATUS_OPTIONS),
        created_at=datetime.now().isoformat(),
    )