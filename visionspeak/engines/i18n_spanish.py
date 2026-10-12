"""
Spanish (es-ES) Localization Pack
"""
from visionspeak.engines.multilingual import MultilingualCaptionAdapter

SPANISH_DICT = {
    "Chasing quiet moments in full color": "Persiguiendo momentos tranquilos a todo color",
    "A frame where the stillness speaks": "Un encuadre donde el silencio habla",
    "Some memories never lose their warmth": "Algunos recuerdos nunca pierden su calidez",
    "Main character energy, no script needed": "Energía de protagonista, sin guión necesario"
}

MultilingualCaptionAdapter.register_dictionary("es", SPANISH_DICT)
