from src.config import (
    CUSTOMERS_PER_RUN,
    PRODUCTS_PER_RUN,
    ORDERS_PER_RUN,
)
from src.logger import logger
from src.pipeline.initial_load import run_initial_load


class BronzePipeline:
    def run(self) -> None:
        logger.info("Executando etapa Bronze.")

        run_initial_load(
            number_of_customers=CUSTOMERS_PER_RUN,
            number_of_products=PRODUCTS_PER_RUN,
            number_of_orders=ORDERS_PER_RUN,
        )

        logger.info("Etapa Bronze concluída.")