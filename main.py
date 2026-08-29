import json
import time
from pathlib import Path

from src.generators.customer_generator import generate_customer
from src.generators.order_generator import generate_order
from src.generators.product_generator import generate_product
from src.loaders.azure_loader import upload_to_azure_lake
from src.loaders.db_loader import save_to_db
from src.logger import logger
from src.models.models import Order
from src.readers.json_reader import JSONReader
from src.transformers.gold_transformer import create_sales_summary

BRONZE_DIR = Path("data/bronze")
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline() -> None:
    logger.info("Iniciando orquestrador de ingestão contínua com Azure Data Lake.")

    products = [generate_product(i) for i in range(1, 21)]
    customers = [generate_customer(i) for i in range(1, 51)]

    # Salva produtos no Data Lake (Bronze)
    products_data = [p.model_dump() for p in products]
    upload_to_azure_lake(products_data, "bronze", "products.json")

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

        # 1. Envia Pedidos em tempo real para a Camada Bronze da Azure
        upload_to_azure_lake(all_orders, "bronze", "orders.json")

        # 2. Leitura e Validação
        reader = JSONReader()
        validated_orders = reader.read(orders_file, Order)

        # 3. Camada Gold (Agregação Parquet) com os produtos já validados
        sales_summary_df = create_sales_summary(validated_orders, products)

        # 4. Envia tabela Gold em formato Parquet para a Azure
        upload_to_azure_lake(sales_summary_df, "gold", "sales_summary.parquet")

        # Mantém gravação local/postgres de segurança
        save_to_db(sales_summary_df, "sales_summary")

        logger.info("Ciclo concluído. Aguardando 15 segundos...")
        time.sleep(15)


if __name__ == "__main__":
    run_pipeline()