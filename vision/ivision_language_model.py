from abc import ABC, abstractmethod


class IVisionLanguageModel(ABC):
    @abstractmethod
    def execute(self, base64_image: str, username: str, formality: str, whoiam: str, todo: str) -> str:
        raise NotImplementedError()
