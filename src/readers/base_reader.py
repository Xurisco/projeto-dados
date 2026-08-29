from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseReader(ABC, Generic[T]):

    @abstractmethod
    def read(self, file_path: Path, model: type[T]) -> list[T]:
        """Método abstrato obrigatório para qualquer leitor de dados."""
        pass