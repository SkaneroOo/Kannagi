from discord.app_commands import Translator as Tr, locale_str, TranslationContextTypes
from discord.enums import Locale

from orjson import loads

from .logger import Logger, LogLevel
import os

logger = Logger(__name__, LogLevel.INFO)

class Translator(Tr):
    
    translations: dict[str, dict[str, str]]

    def __init__(self, translations_path: str):
        self.translations = {}
        self.translations_path = translations_path.strip("/")
    
    async def translate(self, string: locale_str, locale: Locale, context: TranslationContextTypes) -> str | None:
        if locale.value[:2] in self.translations:
            return self.translations[locale.value[:2]].get(string.message, None)
        return None
    
    async def load(self) -> None:
        for file in os.listdir(self.translations_path):
            if file.endswith(".json"):
                self.translations[file[:file.index('.')]] = loads(open(f"{self.translations_path}/{file}", "r").read())
        logger.info("Translations loaded")