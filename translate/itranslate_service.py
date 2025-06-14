from abc import ABC, abstractmethod


class ITranslateService(ABC):
    @abstractmethod
    def translate(self, text: str, source: str, destination: str) -> str:
        raise NotImplementedError()
