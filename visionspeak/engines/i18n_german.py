"""
German (de-DE) Localization Pack
"""
from visionspeak.engines.multilingual import MultilingualCaptionAdapter

GERMAN_DICT = {
    "Chasing quiet moments in full color": "Stille Momente in voller Farbe einfangen",
    "A frame where the stillness speaks": "Ein Bild, in dem die Stille spricht",
    "Some memories never lose their warmth": "Manche Erinnerungen verlieren nie ihre Wärme",
    "Main character energy, no script needed": "Hauptcharakter-Energie, ganz ohne Drehbuch"
}

MultilingualCaptionAdapter.register_dictionary("de", GERMAN_DICT)
