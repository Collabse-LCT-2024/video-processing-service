import asyncio

from processor.tags_processor import TagsProcessor
from src.core.logger import Logger
from src.embedders.labse_embedder import LabseEmbedder
from src.message_router import MessageRouter
from src.services.embedding_aggregator_service import EmbeddingAggregatorService
from src.kafka.consumer import KafkaConsumer

logger = Logger().get_logger()


async def main():
    logger.info("Запуск приложения")

    consumer = KafkaConsumer()
    text_embedder = LabseEmbedder()
    embedding_service = EmbeddingAggregatorService()

    video_processor = TagsProcessor(text_embedder)

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
