"""
Expanded Tone Phrase Matrix (12 Mood Variations)
"""

TONES = {
    "Aesthetic": ["Soft angles and poetic stillness", "Curating my own perspective"],
    "Emotional": ["Holding on to the feeling", "Deep breaths and clear skies"],
    "Inspiring": ["Small steps lead to extraordinary views", "Every frame is a fresh beginning"],
    "Funny": ["My camera had better plans than I did", "Unfiltered reality at its finest"],
    "Moody": ["Shadows tell what light hides", "Quiet storms and velvet evenings"],
    "Romantic": ["A whisper in the afternoon breeze", "Heartbeats and golden sunsets"],
    "Minimalist": ["Less noise, more story", "Space to breathe and just be"],
    "Bold": ["Unapologetically vibrant", "Standing out in every direction"],
    "Nostalgic": ["Echoes of yesterday, alive right now", "Film grain feelings in digital days"],
    "Professional": ["Framed with purpose and precision", "Clear visual storytelling"],
    "Adventure": ["Beyond the edges of the map", "Wild air and open roads"],
    "Cozy": ["Warm corners and slow mornings", "Comfort found in small rituals"]
}

def get_tone_phrases(tone_name: str):
    return TONES.get(tone_name, TONES["Aesthetic"])
