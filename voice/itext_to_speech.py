from abc import ABC, abstractmethod
from typing import Iterator


class ITextToSpeech(ABC):
    @abstractmethod
    def speech(self, text: str) -> Iterator[bytes]:
        raise NotImplementedError()
