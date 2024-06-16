from core.logger import Logger
import os

from utils.frame_extractor import FrameExtractor


class VideoProcessor:
    def __init__(self, video_embedder, text_embedder, frame_extractor: FrameExtractor):
        self.video_embedder = video_embedder
        self.text_embedder = text_embedder
        self.frame_extractor = frame_extractor

        self.logger = Logger().get_logger()

    def process(self, video_id, video_link):

        self.frame_extractor.extract_frames(video_link)

        frame_path = [f"{self.frame_extractor.output_dir}/{frame}" for frame in
                      os.listdir(self.frame_extractor.output_dir)]

        self.logger.info(f"Extracted frames from video {video_id}")

        texts_from_frames = self.video_embedder.embed(frame_path)

        self.logger.info(f"Extracted texts from frames of video {video_id}")

        video_embedding = self.text_embedder.embed(texts_from_frames)

        self.logger.info(f"Extracted embedding from texts of video {video_id}")

        return video_embedding, texts_from_frames
