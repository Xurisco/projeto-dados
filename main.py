import json
import time
from pathlib import Path
import pandas as pd

from src.generators.customer_generator import generate_customer
from src.generators.order_generator import generate_order
from src.generators.product_generator import generate_product
from src.loaders.db_loader import save_to_db
from src.logger import logger
from src.models.models import Order, Product
from src.readers.json_reader import JSONReader
from src.transformers.gold_transformer import create_sales_summary

BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")
GOLD_DIR = Path("data/gold")

BRONZE_DIR.mkdir(parents=True, exist_ok=True)
SILVER_DIR.mkdir(parents=True, exist_ok=True)
GOLD_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline() -> None:
    logger.info("Iniciando orquestrador de ingestão contínua.")

    products = [generate_product(i) for i in range(1, 21)]
    customers = [generate_customer(i) for i in range(1, 51)]

    with open(BRONZE_DIR / "products.json", "w", encoding="utf-8") as f:
        json.dump([p.model_dump() for p in products], f, ensure_ascii=False, indent=2)

    with open(BRONZE_DIR / "customers.json", "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in customers], f, ensure_ascii=False, indent=2)

    order_id_counter = 1

    while True:
        logger.info("--- Novo ciclo de ingestão de dados ---")

        new_orders = [
            generate_order(
                order_id_counter + i,
                [c.id for c in customers],
                products,
            )
            for i in range(10)
        ]
        order_id_counter += 10

        orders_file = BRONZE_DIR / "orders.json"
        existing_orders = []
        if orders_file.exists():
            try:
                with open(orders_file, "r", encoding="utf-8") as f:
                    existing_orders = json.load(f)
            except Exception:
                existing_orders = []

        all_orders = existing_orders + [o.model_dump() for o in new_orders]
        with open(orders_file, "w", encoding="utf-8") as f:
            json.dump(all_orders, f, ensure_ascii=False, indent=2)

        reader = JSONReader()
        validated_orders = reader.read(orders_file, Order)
        validated_products = reader.read(BRONZE_DIR / "products.json", Product)

        sales_summary_df = create_sales_summary(validated_orders, validated_products)

        # Carga de todas as tabelas no PostgreSQL
        save_to_db(sales_summary_df, "sales_summary")
        save_to_db(pd.DataFrame([p.model_dump() for p in validated_products]), "products")
        save_to_db(pd.DataFrame([o.model_dump() for o in validated_orders]), "orders")
        save_to_db(pd.DataFrame([c.model_dump() for c in customers]), "customers")

        logger.info("Ciclo concluído. Aguardando 15 segundos...")
        time.sleep(15)


if __name__ == "__main__":
    run_pipeline()