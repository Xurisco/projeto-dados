from pathlib import Path

import pandas as pd


def save_csv(data: pd.DataFrame, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(file_path, index=False)