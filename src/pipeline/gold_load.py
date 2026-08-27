from pathlib import Path

from src.loaders.csv_loader import save_csv
from src.models.models import Order, Product
from src.readers.json_reader import read_json
from src.transformers.gold_transformer import create_sales_summary


SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")


def run_gold_load() -> None:
    products = read_json(
        SILVER_PATH / "products.json",
        Product,
    )

    orders = read_json(
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