from readers.ireader import IReader
import pytesseract
from PIL import ImageGrab


class OcrScreenshotReader(IReader):
    def __init__(self, lang):
        self.lang = lang

    def read(self) -> str:
        screenshot = ImageGrab.grab()
        return pytesseract.image_to_string(screenshot, lang=self.lang)