import os
import unittest

from utils.vdeo_downloader import VideoDownloader


class TestVideoDownloader(unittest.TestCase):
    def setUp(self):
        self.video_downloader = VideoDownloader()
        self.audio_downloader = VideoDownloader(download_audio_only=True)
        self.test_video_url = "https://cdn-st.rutubelist.ru/media/00/01/6a80bc334457be181c5b83f229de/fhd-wm.mp4"

    def test_download_video(self):
        video_path = self.video_downloader.download(self.test_video_url)
        self.assertIsNotNone(video_path)
        self.assertTrue(os.path.isfile(video_path))

    def test_download_audio(self):
        audio_path = self.audio_downloader.download(self.test_video_url)
        self.assertIsNotNone(audio_path)
        self.assertTrue(os.path.isfile(audio_path))

    def test_download_invalid_url(self):
        with self.assertRaises(Exception) as context:
            self.video_downloader.download("invalid_url")
        self.assertEqual(str(context.exception), "Failed to download video or audio")


if __name__ == "__main__":
    unittest.main()
