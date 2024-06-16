import os

from src.core.logger import Logger


class AudioProcessor:
    def __init__(self, video_downloader, transcriber, text_summarizer, text_embedder):
        self.video_downloader = video_downloader
        self.transcriber = transcriber
        self.text_summarizer = text_summarizer
        self.text_embedder = text_embedder

        self.logger = Logger().get_logger()

    def process(self, video_id, video_link):
        try:
            self.logger.info(f"Audio processor : Downloading video {video_id}")

            v_path = self.video_downloader.download(video_link)

            self.logger.info(f"Audio processor : Transcribing video {video_id}")

            result = self.transcriber.transcribe(v_path)
            lang = self.transcriber.get_language(result)
            text = self.transcriber.get_text(result)

            if text == "":
                os.remove(v_path)
                return None, None, False

            self.logger.info(f"Audio processor : Summarizing text {video_id}")

            res_s_tok = self.text_summarizer.process_text(text, lang)

            self.logger.info(f"Audio processor : Embedding text {video_id}")

            embeddings = self.text_embedder.embed(res_s_tok)

            os.remove(v_path)

            return embeddings, text, True
        except Exception as e:
            self.logger.error(f"Error while processing audio: {e}")
            return None, None, False
