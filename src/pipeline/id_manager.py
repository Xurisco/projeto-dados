from pathlib import Path
import json


class IDManager:
    def __init__(self, path: Path):
        self.path = path

    def get_next_id(self, entity: str) -> int:
        ids = self._load_ids()

        next_id = ids.get(entity, 0) + 1

        ids[entity] = next_id
        self._save_ids(ids)

        return next_id

    def _load_ids(self) -> dict:
        if not self.path.exists():
            return {}

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_ids(self, ids: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(ids, file, indent=2)