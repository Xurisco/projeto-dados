from src.pipeline.initial_load import run_initial_load
from src.pipeline.silver_load import run_silver_load
from src.pipeline.gold_load import run_gold_load


class Pipeline:
    def __init__(self, interval: int = 30):
        self.interval = interval

    def run_once(self) -> None:
        print("\nIniciando pipeline...")

        run_initial_load(
            number_of_customers=10,
            number_of_products=5,
            number_of_orders=50,
        )

        run_silver_load()
        run_gold_load()

        print("Pipeline concluído.")

    def run_forever(self) -> None:
        import time

        while True:
            try:
                self.run_once()

                print(f"Aguardando {self.interval} segundos...")
                time.sleep(self.interval)

            except KeyboardInterrupt:
                print("\nPipeline encerrado.")
                break