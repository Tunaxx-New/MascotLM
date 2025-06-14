from abc import ABC, abstractmethod


class ILargeLanguageModel(ABC):
    @abstractmethod
    def execute(self, text: str, username: str, formality: str, whoiam: str, todo: str) -> str:
        raise NotImplementedError()
