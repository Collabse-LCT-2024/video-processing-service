from uuid import UUID

from core.config import settings
from database.base import DBClient
from qdrant_client import QdrantClient
from qdrant_client.http import models

from models.video_properties import VideoProperties


class QdrantDBClient(DBClient):
    def __init__(self):
        self.qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, grpc_port=settings.QDRANT_GRPC_PORT, prefer_grpc=True)
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def find_by_id(self, item_id: UUID):
        return self.qdrant_client.retrieve(collection_name=self.collection_name, ids=[str(item_id)])

    def save_embedding(self, embedding, properties: VideoProperties):
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(properties.external_id),
                    vector=embedding,
                    payload=properties.to_dict(),
                )
            ],
        )
