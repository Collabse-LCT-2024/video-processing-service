import asyncio

from core.logger import Logger
from database.qdrant_client import QdrantDBClient
from embedders.blip_embedder import BlipEmbedder
from embedders.labse_embedder import LabseEmbedder
from message_router import MessageRouter
from processor.frame_extractor import FrameExtractor
from processor.video_processor import VideoProcessor
from src.kafka.consumer import KafkaConsumer

logger = Logger().get_logger()


async def main():
    logger.info("Запуск приложения")

    consumer = KafkaConsumer()
    video_embedder = BlipEmbedder()
    text_embedder = LabseEmbedder()
    db_client = QdrantDBClient()
    frame_extractor = FrameExtractor("frames")

    video_processor = VideoProcessor(video_embedder, text_embedder, frame_extractor)

    router = MessageRouter(video_processor, db_client)

    try:
        async for messages in consumer.consume_messages():
            for msg in messages:
                await router.route_message(msg)
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке сообщений: {e}")
    finally:
        logger.info("Приложение завершает работу.")


if __name__ == "__main__":
    asyncio.run(main())
