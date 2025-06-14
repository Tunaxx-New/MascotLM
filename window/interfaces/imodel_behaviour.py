from abc import ABC, abstractmethod

class IModelBehaviour(ABC):
    @abstractmethod
    def speech(self, text: str) -> None:
        """Display a popup with the given text."""
        raise NotImplementedError()
