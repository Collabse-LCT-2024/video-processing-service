import json

from aiokafka import ConsumerRecord

from core.logger import Logger
from database.base import DBClient
from models.events import KafkaUploadedEvent
from models.video_properties import VideoProperties


class MessageRouter:
    def __init__(self, video_processor, db_client: DBClient):
        self.video_processor = video_processor
        self.db_client = db_client
        self.logger = Logger().get_logger()

    async def route_message(self, msg: ConsumerRecord):
        message = json.loads(msg.value.decode("utf-8"))
        event = KafkaUploadedEvent(**message)

        video_id = event.video_id
        video_url = event.video_url

        if self.db_client.find_by_id(video_id):
            self.logger.info(f"Видео {video_id} уже обработано")
            return

        video_embedding, video_text = self.video_processor.process(video_id, video_url)

        video_properties = VideoProperties(
            external_id=video_id,
            link=video_url,
            text=video_text,
        )

        self.db_client.save_embedding(video_embedding, video_properties)

