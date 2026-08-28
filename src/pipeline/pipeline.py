import time

from src.config import PIPELINE_INTERVAL
from src.logger import logger
from src.pipeline.bronze_pipeline import BronzePipeline
from src.pipeline.silver_pipeline import SilverPipeline
from src.pipeline.gold_pipeline import GoldPipeline


class Pipeline:
    def __init__(self, interval: int = PIPELINE_INTERVAL):
        self.interval = interval

        self.bronze = BronzePipeline()
        self.silver = SilverPipeline()
        self.gold = GoldPipeline()

    def run_once(self) -> None:
        logger.info("Iniciando pipeline.")

        try:
            self.bronze.run()
            self.silver.run()
            self.gold.run()

            logger.info("Pipeline concluído.")

        except Exception:
            logger.exception("Erro durante a execução do pipeline.")

    def run_forever(self) -> None:
        while True:
            try:
                self.run_once()

                logger.info(
                    "Aguardando %s segundos.",
                    self.interval,
                )

                time.sleep(self.interval)

            except KeyboardInterrupt:
                logger.info("Pipeline encerrado.")
                break