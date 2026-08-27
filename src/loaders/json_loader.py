import json
from pathlib import Path

from pydantic import BaseModel


def save_json(data: list[BaseModel], file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    records = [item.model_dump(mode="json") for item in data]

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)