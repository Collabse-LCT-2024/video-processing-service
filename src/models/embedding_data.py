from dataclasses import dataclass
from uuid import UUID


@dataclass
class EmbeddingData:
    video_id: UUID
    embedding: list[float]
    video_url: str
    text: str
    collection: str

    def to_dict(self):
        return {
            "video_id": str(self.video_id),
            "embedding": self.embedding,
            "video_url": self.video_url,
            "text": '.'.join(self.text),
            "collection": self.collection
        }