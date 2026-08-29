import json
from pathlib import Path

from src.generators.customer_generator import generate_customer
from src.generators.data_quality_injector import DataQualityInjector
from src.generators.order_generator import generate_order
from src.generators.product_generator import generate_product
from src.loaders.json_loader import JSONLoader
from src.pipeline.id_manager import IDManager

BRONZE_PATH = Path("data/bronze")
ID_MANAGER = IDManager(Path("data/metadata/ids.json"))
JSON_LOADER = JSONLoader()


def run_initial_load(
    number_of_customers: int,
    number_of_products: int,
    number_of_orders: int,
) -> None:
    customers = [
        generate_customer(ID_MANAGER.get_next_id("customer"))
        for _ in range(number_of_customers)
    ]

    products = [
        generate_product(ID_MANAGER.get_next_id("product"))
        for _ in range(number_of_products)
    ]

    customer_ids = [customer.id for customer in customers]

    orders = [
        generate_order(
            ID_MANAGER.get_next_id("order"),
            customer_ids,
            products,
        )
        for _ in range(number_of_orders)
    ]

    # Injeta inconsistências nos pedidos
    dirty_orders = DataQualityInjector.inject_dirty_orders(orders)

    JSON_LOADER.save(customers, BRONZE_PATH / "customers.json")
    JSON_LOADER.save(products, BRONZE_PATH / "products.json")

    # Salva os pedidos brutos contendo dados problemáticos
    file_path = BRONZE_PATH / "orders.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            existing = json.load(f)
    existing.extend(dirty_orders)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)