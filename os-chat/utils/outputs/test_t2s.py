import os.path

import pytest

from utils.outputs.text_to_speech import TextToSpeechConfig, text_to_speech

config = TextToSpeechConfig(text='hello', output="testcache/output.mp3")


def test_t2s():
    text_to_speech(config)

    assert os.path.exists(config.output) is True


@pytest.fixture(scope='session', autouse=True)
def cleanup():
    filename = config.output
    print("Performing cleanup tasks before running tests")
    if not os.path.exists(filename):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname): os.mkdir(dirname)
    else:
        os.remove(filename)

    yield
    temp_files = [filename]
    print("Performing cleanup tasks after running tests")
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
