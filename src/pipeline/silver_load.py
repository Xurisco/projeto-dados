from pathlib import Path

from src.loaders.json_loader import JSONLoader
from src.models.models import Customer, Product
from src.readers.json_reader import JSONReader
from src.transformers.data_quality import DataQualityValidator
from src.transformers.data_transformer import (
    transform_customers,
    transform_products,
    transform_orders,
)

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")

JSON_READER = JSONReader()
JSON_LOADER = JSONLoader()


def run_silver_load() -> None:
    customers = JSON_READER.read(
        BRONZE_PATH / "customers.json",
        Customer,
    )

    products = JSON_READER.read(
        BRONZE_PATH / "products.json",
        Product,
    )

    # Aplica validação de Data Quality nos Pedidos brutos
    orders = DataQualityValidator.validate_and_clean_orders(
        BRONZE_PATH / "orders.json"
    )

    customers = transform_customers(customers)
    products = transform_products(products)
    orders = transform_orders(orders)

    JSON_LOADER.save(customers, SILVER_PATH / "customers.json")
    JSON_LOADER.save(products, SILVER_PATH / "products.json")
    JSON_LOADER.save(orders, SILVER_PATH / "orders.json")