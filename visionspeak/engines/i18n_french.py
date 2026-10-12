"""
French (fr-FR) Localization Pack
"""
from visionspeak.engines.multilingual import MultilingualCaptionAdapter

FRENCH_DICT = {
    "Chasing quiet moments in full color": "À la recherche de moments calmes en pleine couleur",
    "A frame where the stillness speaks": "Un cadre où le silence s'exprime",
    "Some memories never lose their warmth": "Certains souvenirs ne perdent jamais leur chaleur",
    "Main character energy, no script needed": "Énergie de protagoniste, sans scénario nécessaire"
}

MultilingualCaptionAdapter.register_dictionary("fr", FRENCH_DICT)
