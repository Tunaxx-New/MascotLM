import math
import tempfile
from abc import ABC, abstractmethod
from io import BytesIO
import pyaudio
from typing import Iterator
from pydub import AudioSegment
from pydub.playback import play


class ISoundService(ABC):
    @abstractmethod
    def play(self, stream: Iterator[bytes], volume: float) -> None:
        raise NotImplementedError()

class SoundService(ISoundService):
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()

    def play(self, stream: Iterator[bytes], volume: float) -> None:
        full_bytes = b"".join(stream)
        audio = AudioSegment.from_file(BytesIO(full_bytes), format="mp3")

        # Calculate dB change for volume multiplier
        if volume > 0:
            db_change = 20 * math.log10(volume)
        else:
            db_change = -120  # mute

        # Apply volume change
        audio = audio + db_change

        # Play audio directly
        play(audio)