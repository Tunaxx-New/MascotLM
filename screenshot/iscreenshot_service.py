import base64
from abc import ABC, abstractmethod
from io import BytesIO
from PIL import ImageGrab


class IScreenshotService(ABC):
    @abstractmethod
    def base64_image(self) -> str:
        raise NotImplementedError()

class ScreenshotService(IScreenshotService):
    def base64_image(self) -> str:
        screenshot = ImageGrab.grab()
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")