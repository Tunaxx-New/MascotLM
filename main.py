import asyncio
import os
import random
import threading
from time import sleep

from dotenv import load_dotenv

from conversation import ILargeLanguageModel, HuggingFaceLargeLanguageModelService, LlamaLargeModelModel
from readers import OcrScreenshotReader, IReader
from screenshot import IScreenshotService, ScreenshotService
from sound import ISoundService, SoundService
from translate import ITranslateService, GoogleTranslateService
from vision import HuggingFaceVisionLanguageModelService, IVisionLanguageModel
from voice import EvenLabsService, ITextToSpeech
from web import run_flask
from window import create_app
from window.interfaces.iapp import IApp
from window.interfaces.imodel_behaviour import IModelBehaviour

def random_conversation(choice_not: list[int] = [0], choice: int = None) -> str:
    if not choice:
        choice = random.randint(1, 3)
    if choice in choice_not:
        random_conversation(choice_not)

    if choice == 1:
        try:
             return vision_service.execute(
                screenshot_service.base64_image(),
                os.getenv('USERNAME_CALL'),
                os.getenv('FORMALITY'),
                os.getenv('WHOIAM'),
                os.getenv('TODO')
            )
        except Exception as e:
            print(e)
            if 1 not in choice_not:
                choice_not.append(1)
            random_conversation(choice_not)
    elif choice == 2:
        # Screenshot conversation
        try:
            return conversation_service.execute(
                'On screen you see: ' + screen_reader.read(),
                os.getenv('USERNAME_CALL'),
                os.getenv('FORMALITY'),
                os.getenv('WHOIAM'),
                os.getenv('TODO'))
        except Exception:
            if 2 not in choice_not:
                choice_not.append(2)
            random_conversation(choice_not)
    elif choice == 3:
        # Screenshot conversation
        conversation_service.execute(
            'On screen you see: ' + screen_reader.read(),
            os.getenv('USERNAME_CALL'),
            os.getenv('FORMALITY'),
            os.getenv('WHOIAM'),
            os.getenv('TODO'))


# Free quota for Hugging Face VLM

def periodic_task():
    while True:
        # --- Thinking ---
        message = random_conversation(choice=1)
        # ---          ---

        # --- Speaking ---
        message = translate_service.translate(message, os.getenv('TRANSLATE_SOURCE'), os.getenv('TRANSLATE_DESTINATION'))
        def play_sound():
            try:
                sound_service.play(voice_service.speech(message), float(os.getenv('EL_VOLUME')))
            except Exception:
                # Free quota for evenlabs API
                pass
        threading.Thread(target=play_sound, daemon=True).start()
        model_window.speech(message)
        # ---          ---

        sleep(300)

if __name__ == '__main__':
    load_dotenv()
    flask_thread_flask = threading.Thread(target=run_flask, args=(int(os.getenv('WEB_PORT')),), daemon=True).start()

    model_window: IModelBehaviour
    app: IApp
    model_window, app = create_app(
        int(os.getenv('WINDOW_WIDTH')),
        int(os.getenv('WINDOW_HEIGHT')),
        int(os.getenv('WEB_PORT')),
        os.getenv('SHOW_HIDE_KEY'),
        int(os.getenv('POPUP_TIMEOUT_MS')),
        os.getenv('POPUP_DESTOROOT_KEY'),
    )

    translate_service: ITranslateService = GoogleTranslateService()
    vision_service: IVisionLanguageModel = HuggingFaceVisionLanguageModelService(os.getenv('HF_API_KEY'), os.getenv('VLM_NAME'))
    conversation_service: ILargeLanguageModel = LlamaLargeModelModel(os.getenv('LLM_NAME'), os.getenv('HF_CACHE_DIR'))
    screenshot_service: IScreenshotService = ScreenshotService()
    voice_service: ITextToSpeech = EvenLabsService(os.getenv('EL_API_KEY'), os.getenv('EL_VOICE_ID'), os.getenv('EL_MODEL_NAME'))
    sound_service: ISoundService = SoundService()
    screen_reader: IReader = OcrScreenshotReader(os.getenv('OCR_READ_LANGUAGES'))

    flask_thread_task = threading.Thread(target=periodic_task, daemon=True).start()

    app.start()
