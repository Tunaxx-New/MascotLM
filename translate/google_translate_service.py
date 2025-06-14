import asyncio
from googletrans import Translator

from translate.itranslate_service import ITranslateService


class GoogleTranslateService(ITranslateService):
    def __init__(self) -> None:
        self.translator = Translator()

    def translate(self, text: str, source: str, destination: str) -> str:
        return asyncio.run(self.translator.translate(text, src=source, dest=destination)).text
