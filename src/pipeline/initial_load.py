from pathlib import Path

from src.generators.customer_generator import generate_customer
from src.generators.order_generator import generate_order
from src.generators.product_generator import generate_product
from src.loaders.json_loader import save_json


BRONZE_PATH = Path("data/bronze")


def run_initial_load(
    number_of_customers: int,
    number_of_products: int,
    number_of_orders: int,
) -> None:
    customers = [
        generate_customer(customer_id)
        for customer_id in range(1, number_of_customers + 1)
    ]

    products = [
        generate_product(product_id)
        for product_id in range(1, number_of_products + 1)
    ]

    customer_ids = [customer.id for customer in customers]

    orders = [
        generate_order(order_id, customer_ids, products)
        for order_id in range(1, number_of_orders + 1)
    ]

    save_json(customers, BRONZE_PATH / "customers.json")
    save_json(products, BRONZE_PATH / "products.json")
    save_json(orders, BRONZE_PATH / "orders.json")