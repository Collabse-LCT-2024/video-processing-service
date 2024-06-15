import requests
from abc import ABC, abstractmethod

from src.models.embedding_data import EmbeddingData


class EmbeddingServiceABC(ABC):
    @abstractmethod
    def send_embedding(self, data: EmbeddingData) -> requests.Response:
        pass
