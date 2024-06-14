import os
import shutil
import pytest

from processor.frame_extractor import FrameExtractor


@pytest.fixture
def frame_extractor(tmpdir):
    output_dir = tmpdir.mkdir("output")
    print(f"Temporary directory: {output_dir.strpath}")
    return FrameExtractor(output_dir.strpath)


def test_extract_frames(frame_extractor):
    video_link = "https://cdn-st.rutubelist.ru/media/00/00/4514d5cc44bc92590da5c08236c1/fhd-wm.mp4"

    n = 10
    width = 299
    height = 299

    frame_extractor.extract_frames(video_link, n, width, height)

    # Проверяем, что в выходной директории созданы кадры
    output_files = os.listdir(frame_extractor.output_dir)
    assert len(output_files) > 0

    # Проверяем, что кадры имеют правильное расширение
    for file in output_files:
        assert file.endswith(".png")

    # Проверяем, что кадры имеют правильный размер
    for file in output_files:
        file_path = os.path.join(frame_extractor.output_dir, file)
        assert os.path.getsize(file_path) > 0

    # Очищаем временную директорию после теста
    shutil.rmtree(frame_extractor.output_dir)
