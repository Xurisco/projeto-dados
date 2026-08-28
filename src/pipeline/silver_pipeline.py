from src.pipeline.silver_load import run_silver_load


class SilverPipeline:
    def run(self) -> None:
        run_silver_load()