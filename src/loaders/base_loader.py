from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseLoader(ABC):

    @abstractmethod
    def save(self, data: Any, destination: Any) -> None:
        
        pass