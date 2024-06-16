import os


class AudioProcessor:
    def __init__(self, video_downloader, transcriber, text_summarizer, text_embedder):
        self.video_downloader = video_downloader
        self.transcriber = transcriber
        self.text_summarizer = text_summarizer
        self.text_embedder = text_embedder

    def process(self, video_id, video_link):
        try:
            v_path = self.video_downloader.download(video_link)
            result = self.transcriber.transcribe(v_path)
            lang = self.transcriber.get_language(result)
            text = self.transcriber.get_text(result)

            if text == "":
                os.remove(v_path)
                raise Exception("Empty transcript")

            res_s_tok = self.text_summarizer.process_text(text, lang)

            embeddings = self.text_embedder.embed(res_s_tok)

            os.remove(v_path)

            return embeddings, text
        except Exception as e:
            print(f"Error processing video {video_id}: {str(e)}")
            raise e