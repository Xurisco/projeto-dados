from src.pipeline.pipeline import Pipeline


if __name__ == "__main__":
    pipeline = Pipeline(interval=30)
    pipeline.run_forever()