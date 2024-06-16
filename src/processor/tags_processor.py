import re

from core.logger import Logger


class TagsProcessor:
    def __init__(self, text_embedder):
        self.text_embedder = text_embedder
        self.logger = Logger().get_logger()

    def process(self, video_id, description):

        tags = re.findall(r"#\w+", description)

        if len(tags) == 0:
            self.logger.info(f"Video {video_id} has no tags")
            return

        self.logger.info(f"Extracted tags from video {video_id}")

        tags = " ".join(tags).replace("#", "")

        tags_embedding = self.text_embedder.embed(tags.split(" "))

        self.logger.info(f"Done embedding tags for video {video_id}")

        return tags_embedding, tags
