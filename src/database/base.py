from typing import List
from uuid import UUID
from abc import ABC, abstractmethod

from models.video_properties import VideoProperties


class DBClient(ABC):
    @abstractmethod
    def find_by_id(self, item_id: UUID) -> List[UUID]:
        pass

    @abstractmethod
    def save_embedding(self, embedding, properties: VideoProperties):
        pass

