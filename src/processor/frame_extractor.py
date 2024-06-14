from core.logger import Logger
import os
import ffmpeg


class FrameExtractor:
    def __init__(self, output_dir):
        self.logger = Logger().get_logger()
        self.output_dir = output_dir
        self.platform = os.name

        if self.platform == "nt":
            self.ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe")
        else:
            self.ffmpeg_path = "ffmpeg"

    def extract_frames(self, video_link, n: int = 15, width: int = 299, height: int = 299):
        output_pattern = os.path.join(self.output_dir, "frame_%04d.png")
        (
            ffmpeg.input(video_link)
            .filter("select", f"not(mod(n,{n}))")
            .filter("scale", width=width, height=height)
            .output(output_pattern, vsync="vfr")
            .global_args(
                "-loglevel", "error"
            )  # Add this line to suppress FFmpeg output
            .run(cmd=self.ffmpeg_path, capture_stdout=True, capture_stderr=True)
        )

        self.logger.info(f"Extracting frames from video {video_link}")