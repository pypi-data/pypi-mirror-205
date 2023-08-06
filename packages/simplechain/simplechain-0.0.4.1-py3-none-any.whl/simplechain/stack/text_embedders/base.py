from abc import ABC, abstractmethod
from typing import List

import numpy as np
from pydantic import BaseModel


class TextEmbedder(BaseModel, ABC):
    @abstractmethod
    def embed(self, text:  str) -> np.ndarray:
        pass

    @abstractmethod
    def embed_all(self, texts: List[str]) -> List[np.ndarray]:
        pass


