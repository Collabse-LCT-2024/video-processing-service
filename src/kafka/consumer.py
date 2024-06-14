from aiokafka import AIOKafkaConsumer

from core.config import settings


class KafkaConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            settings.kafka_video_processing_requests_topic,
            bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}"
        )

    async def consume_messages(self):
        await self.consumer.start()
        try:
            while True:
                result = await self.consumer.getmany(timeout_ms=1000, max_records=1000)
                for tp, messages in result.items():
                    yield messages
        finally:
            await self.consumer.stop()
