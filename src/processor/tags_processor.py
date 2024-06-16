import re

from src.core.logger import Logger


class TagsProcessor:
    def __init__(self, text_embedder):
        self.text_embedder = text_embedder
        self.logger = Logger().get_logger()

    def process(self, video_id, description):

        tags = re.findall(r"#\w+", description)

        if len(tags) == 0:
            self.logger.info(f"Tags processor : No tags found for video {video_id}")
            return None, None, False

        tags = " ".join(tags).replace("#", "")

        self.logger.info(f"Tags processor : Embedding tags for video {video_id}")

        tags_embedding = self.text_embedder.embed(tags.split(" "))

        return tags_embedding, tags, True
