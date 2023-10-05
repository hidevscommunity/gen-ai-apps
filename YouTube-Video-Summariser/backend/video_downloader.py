from pytube import YouTube
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_video(url):
    logger = logging.getLogger(f"{__name__}.download_video")
    yt = YouTube(url)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    destination = "data/"

    # download the file
    out_file = video.download(output_path=destination)

    # clean existing files
    logger.info("deleting data/audio.mp3")
    try:
        os.remove("data/audio.mp3")
    except FileNotFoundError:
        pass

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = "data/audio.mp3"
    os.rename(out_file, new_file)

    # result of success
    logger.info(yt.title + " has been successfully downloaded.")
    return yt.title


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=VjqZDXTkMAI"
    download_video(video_url)
