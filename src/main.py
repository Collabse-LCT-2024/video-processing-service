import asyncio

from src.core.logger import Logger
from src.embedders.blip_embedder import BlipEmbedder
from src.embedders.labse_embedder import LabseEmbedder
from src.message_router import MessageRouter
from src.processor.frame_extractor import FrameExtractor
from src.processor.video_processor import VideoProcessor
from src.services.embedding_aggregator_service import EmbeddingAggregatorService
from src.kafka.consumer import KafkaConsumer

logger = Logger().get_logger()


async def main():
    logger.info("Запуск приложения")

    consumer = KafkaConsumer()
    video_embedder = BlipEmbedder()
    text_embedder = LabseEmbedder()
    embedding_service = EmbeddingAggregatorService()
    frame_extractor = FrameExtractor("frames")

    video_processor = VideoProcessor(video_embedder, text_embedder, frame_extractor)

    router = MessageRouter(video_processor, embedding_service)

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
