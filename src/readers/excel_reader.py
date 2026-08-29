from pathlib import Path
from typing import TypeVar

import pandas as pd
from pydantic import BaseModel
from src.readers.base_reader import BaseReader

T = TypeVar("T", bound=BaseModel)


class ExcelReader(BaseReader[T]):

    def read(self, file_path: Path, model: type[T]) -> list[T]:
        df = pd.read_excel(file_path)
        records = df.to_dict(orient="records")
        return [model.model_validate(item) for item in records]