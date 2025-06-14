from typing import Iterator

from elevenlabs.client import ElevenLabs

from voice.itext_to_speech import ITextToSpeech


class EvenLabsService(ITextToSpeech):
    def __init__(self, api_key: str, voice_id: str, model_id: str, volume: float = 1.0, output_format: str = "mp3_44100_128"):
        self.elevenlabs = ElevenLabs(
            api_key=api_key,
        )
        self.voice_id = voice_id
        self.model_id = model_id
        self.output_format = output_format
        self.volume = volume

    def speech(self, text: str) -> Iterator[bytes]:
        return self.elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format=self.output_format,
        )
