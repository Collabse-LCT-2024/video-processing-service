import asyncio

from src.embedders.whisper_transcriber import WhisperTranscriber
from src.processor.audio_precessor import AudioProcessor
from src.core.logger import Logger
from src.embedders.labse_embedder import LabseEmbedder
from src.message_router import MessageRouter
from src.services.embedding_aggregator_service import EmbeddingAggregatorService
from src.kafka.consumer import KafkaConsumer
from src.utils.nltk_tokenizer import NLTKTokenizer
from src.utils.text_summarizer import TextSummarizer
from src.utils.vdeo_downloader import VideoDownloader

logger = Logger().get_logger()


async def main():
    logger.info("Audio processing service started.")

    consumer = KafkaConsumer()
    embedding_service = EmbeddingAggregatorService()

    video_downloader = VideoDownloader()
    transcriber = WhisperTranscriber()
    tokenizer = NLTKTokenizer()
    text_summarizer = TextSummarizer(tokenizer)
    text_embedder = LabseEmbedder()
    audio_processor = AudioProcessor(
        video_downloader,
        transcriber,
        text_summarizer,
        text_embedder
    )

    router = MessageRouter(audio_processor, embedding_service)

    try:
        async for messages in consumer.consume_messages():
            for msg in messages:
                await router.route_message(msg)
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        logger.info("Video processing service stopped.")


if __name__ == "__main__":
    asyncio.run(main())
