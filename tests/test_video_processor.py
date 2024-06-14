import os
import shutil

import numpy as np
from embedders.blip_embedder import BlipEmbedder
from embedders.labse_embedder import LabseEmbedder
from processor.frame_extractor import FrameExtractor
from processor.video_processor import VideoProcessor


def test_process(tmpdir):
    video_id = "test_video"
    video_link = "https://cdn-st.rutubelist.ru/media/00/00/4514d5cc44bc92590da5c08236c1/fhd-wm.mp4"

    output_dir = tmpdir.mkdir("output")
    video_embedder = BlipEmbedder()
    text_embedder = LabseEmbedder()
    frame_extractor = FrameExtractor(output_dir.strpath)
    video_processor = VideoProcessor(video_embedder, text_embedder, frame_extractor)

    video_embedding, video_text = video_processor.process(video_id, video_link)

    # print(video_embedding)
    print(video_text)

    # Проверяем, что возвращаемые значения имеют правильный тип и размерность
    assert isinstance(video_embedding, np.ndarray)
    assert video_embedding.shape == (768,)
    assert isinstance(video_text, list)
    assert len(video_text) > 0
    assert isinstance(video_text[0], str)

    # Проверяем, что кадры были извлечены и сохранены
    frames_path = video_processor.frame_extractor.output_dir
    assert os.path.exists(frames_path)
    assert len(os.listdir(frames_path)) > 0

    # Очищаем временную директорию после теста
    shutil.rmtree(tmpdir)
