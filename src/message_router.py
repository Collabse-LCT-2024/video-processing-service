import json

from aiokafka import ConsumerRecord

from src.core.config import settings
from src.core.logger import Logger
from src.models.events import KafkaUploadedEvent
from src.models.embedding_data import EmbeddingData
from src.services.base import EmbeddingServiceABC


class MessageRouter:
    def __init__(self, video_processor, embedding_service: EmbeddingServiceABC):
        self.video_processor = video_processor
        self.embedding_service = embedding_service
        self.logger = Logger().get_logger()

    async def route_message(self, msg: ConsumerRecord):
        try:

            message = json.loads(msg.value.decode("utf-8"))
            event = KafkaUploadedEvent(**message)

            video_id = event.video_id
            video_url = event.video_url

            self.logger.info(f"Start processing video {video_id}")

            video_embedding, video_text = self.video_processor.process(video_id, video_url)

            video_properties = EmbeddingData(
                video_id=video_id,
                embedding=video_embedding.tolist(),
                video_url=video_url,
                text=video_text,
                valid=True,
                description=event.video_desc,
                collection=settings.QDRANT_COLLECTION_NAME
            )

            self.embedding_service.send_embedding(video_properties)

            self.logger.info(f"Successfully processed video {video_id}")

        except Exception as e:
            self.logger.error(f"Error while processing video: {e}")
