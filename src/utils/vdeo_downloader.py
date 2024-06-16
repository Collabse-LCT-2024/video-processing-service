import os
import youtube_dl


class VideoDownloader:
    def __init__(self, download_audio_only=False):
        self.download_audio_only = download_audio_only

    def _download_video_or_audio(self, link: str, download_audio_only: bool = False):
        ydl_opts = {}
        output_path = None

        def my_hook(d):
            nonlocal output_path
            if d['status'] == 'finished':
                file_path = d['filename']
                if download_audio_only:
                    output_path = file_path.rsplit(".", 1)[0] + ".mp3"
                else:
                    output_path = file_path

        if download_audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'videos/%(title)s.%(ext)s',
                'progress_hooks': [my_hook],
                'quiet': True,
            })
        else:
            ydl_opts.update({
                'format': 'best',
                'outtmpl': 'videos/%(title)s.%(ext)s',
                'progress_hooks': [my_hook],
                'quiet': True,
            })

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return output_path

    def download(self, link):
        try:
            v_path = self._download_video_or_audio(link, download_audio_only=self.download_audio_only)
            return v_path
        except Exception:
            if os.path.isfile("videos\fhd-wm.mp4"):
                os.remove("videos\fhd-wm.mp4")
            if os.path.isfile("videos\fhd-wm.mp3"):
                os.remove("videos\fhd-wm.mp3")
            raise Exception("Failed to download video or audio")
