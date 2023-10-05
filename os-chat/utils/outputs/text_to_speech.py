import io
from pathlib import Path

from gtts import gTTS

from dataclasses import dataclass


@dataclass(slots=True)
class TextToSpeechConfig:
    text: str
    output: str | io.BytesIO | Path
    tld: str = 'com'
    lang: str = "en"
    slow: bool = False
    format: str = "audio/mp3"


def text_to_speech(config: TextToSpeechConfig):
    tts = gTTS(text=config.text,
               lang=config.lang,
               slow=config.slow,
               tld=config.tld, )

    out = config.output
    if isinstance(out, str) or isinstance(out, Path):
        tts.save(out)
    elif isinstance(out, io.BytesIO):
        tts.write_to_fp(out)
    else:
        raise ValueError("invalid format")
