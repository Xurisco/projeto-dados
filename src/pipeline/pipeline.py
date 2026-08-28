from src.config import PIPELINE_INTERVAL
from src.pipeline.bronze_pipeline import BronzePipeline
from src.pipeline.silver_pipeline import SilverPipeline
from src.pipeline.gold_pipeline import GoldPipeline
import time


class Pipeline:
    def __init__(self, interval: int = PIPELINE_INTERVAL):
        self.interval = interval

        self.bronze = BronzePipeline()
        self.silver = SilverPipeline()
        self.gold = GoldPipeline()

    def run_once(self) -> None:
        print("\nIniciando pipeline...")

        self.bronze.run()
        self.silver.run()
        self.gold.run()

        print("Pipeline concluído.")

    def run_forever(self) -> None:
        while True:
            try:
                self.run_once()

                print(f"Aguardando {self.interval} segundos...")
                time.sleep(self.interval)

            except KeyboardInterrupt:
                print("\nPipeline encerrado.")
                break