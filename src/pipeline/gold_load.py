from pathlib import Path

from src.loaders.csv_loader import save_csv
from src.loaders.db_loader import save_to_db
from src.models.models import Order, Product
from src.readers.json_reader import JSONReader
from src.transformers.gold_transformer import create_sales_summary

SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")

JSON_READER = JSONReader()


def run_gold_load() -> None:
    products = JSON_READER.read(
        SILVER_PATH / "products.json",
        Product,
    )

    orders = JSON_READER.read(
        SILVER_PATH / "orders.json",
        Order,
    )

    sales_summary = create_sales_summary(
        orders,
        products,
    )

    save_csv(
        sales_summary,
        GOLD_PATH / "sales_summary.csv",
    )

    save_to_db(
        sales_summary,
        table_name="sales_summary",
    )