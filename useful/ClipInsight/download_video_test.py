import os
import unittest
from app import download_video

class TestDownloadVideo(unittest.TestCase):
    
    def test_download_video(self):
        url = "https://www.youtube.com/watch?v=R2nr1uZ8ffc"
        result = download_video(url)
        base, extension = os.path.splitext(result)
        print(f"base: ${base}")
        self.assertEqual(extension, '.mp3');