from src.pipeline.pipeline import Pipeline


def test_pipeline_initialization():
    pipeline = Pipeline(interval=10)

    assert pipeline.interval == 10
    assert pipeline.bronze is not None
    assert pipeline.silver is not None
    assert pipeline.gold is not None