import json
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


def read_json(file_path: Path, model: type[T]) -> list[T]:
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [model.model_validate(item) for item in data]