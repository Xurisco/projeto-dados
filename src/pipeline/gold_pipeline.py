from src.pipeline.gold_load import run_gold_load


class GoldPipeline:
    def run(self) -> None:
        run_gold_load()