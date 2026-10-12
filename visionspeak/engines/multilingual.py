"""
Offline Multilingual Caption Translation Dictionary Framework
"""
from enum import Enum
from typing import Dict, Any

class SupportedLanguage(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    HINDI = "hi"
    JAPANESE = "ja"

class MultilingualCaptionAdapter:
    DICTIONARIES: Dict[str, Dict[str, str]] = {}

    @classmethod
    def register_dictionary(cls, lang_code: str, dictionary: Dict[str, str]):
        cls.DICTIONARIES[lang_code] = dictionary

    @classmethod
    def translate(cls, phrase: str, target_lang: str) -> str:
        lang_dict = cls.DICTIONARIES.get(target_lang, {})
        return lang_dict.get(phrase, phrase)
