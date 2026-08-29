import json
from pathlib import Path

from pydantic import BaseModel
from src.loaders.base_loader import BaseLoader


class JSONLoader(BaseLoader):

    def save(self, data: list[BaseModel], file_path: Path) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        records = [item.model_dump(mode="json") for item in data]
        existing_records = []

        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as file:
                existing_records = json.load(file)

        existing_records.extend(records)

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                existing_records,
                file,
                ensure_ascii=False,
                indent=2,
            )