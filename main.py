from src.pipeline.initial_load import run_initial_load
from src.pipeline.silver_load import run_silver_load
from src.pipeline.gold_load import run_gold_load


if __name__ == "__main__":
    run_initial_load(
        number_of_customers=100,
        number_of_products=50,
        number_of_orders=500,
    )

    run_silver_load()
    run_gold_load()