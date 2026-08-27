from pathlib import Path

from src.loaders.json_loader import save_json
from src.models.models import Customer, Product, Order
from src.readers.json_reader import read_json
from src.transformers.data_transformer import (
    transform_customers,
    transform_products,
    transform_orders,
)


BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")


def run_silver_load() -> None:
    customers = read_json(
        BRONZE_PATH / "customers.json",
        Customer,
    )

    products = read_json(
        BRONZE_PATH / "products.json",
        Product,
    )

    orders = read_json(
        BRONZE_PATH / "orders.json",
        Order,
    )

    customers = transform_customers(customers)
    products = transform_products(products)
    orders = transform_orders(orders)

    save_json(customers, SILVER_PATH / "customers.json")
    save_json(products, SILVER_PATH / "products.json")
    save_json(orders, SILVER_PATH / "orders.json")