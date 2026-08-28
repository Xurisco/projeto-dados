from src.logger import logger
from src.pipeline.silver_load import run_silver_load


class SilverPipeline:
    def run(self) -> None:
        logger.info("Executando etapa Silver.")

        run_silver_load()

        logger.info("Etapa Silver concluída.")