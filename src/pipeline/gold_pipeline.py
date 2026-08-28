from src.logger import logger
from src.pipeline.gold_load import run_gold_load


class GoldPipeline:
    def run(self) -> None:
        logger.info("Executando etapa Gold.")

        run_gold_load()

        logger.info("Etapa Gold concluída.")