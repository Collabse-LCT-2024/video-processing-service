import requests

from src.core.config import settings
from src.models.embedding_data import EmbeddingData
from src.services.base import EmbeddingServiceABC


class EmbeddingAggregatorService(EmbeddingServiceABC):
    def __init__(self, api_url: str = settings.EMBEDDING_API_URL):
        self.api_url = api_url

    def send_embedding(self, data: EmbeddingData) -> requests.Response:
        response = requests.post(self.api_url, json=data.to_dict())
        response.raise_for_status()
        return response

