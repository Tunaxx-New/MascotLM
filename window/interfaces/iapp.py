from abc import ABC, abstractmethod

class IApp(ABC):
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError()
