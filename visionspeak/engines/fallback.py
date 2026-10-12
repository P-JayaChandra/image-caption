"""
Deterministic Fallback Caption Orchestrator
"""
import hashlib
from PIL import Image
from visionspeak.engines.hashing import PerceptualHasher
from visionspeak.engines.color_analysis import ColorAnalyzer
from visionspeak.engines.composition import CompositionClassifier

class FallbackCaptionEngine:
    @classmethod
    def generate(cls, image: Image.Image, filename: str = "moment.jpg", category: str = "General", tone: str = "Aesthetic"):
        dhash = PerceptualHasher.compute_dhash(image)
        colors = ColorAnalyzer.extract_palette(image)
        comp = CompositionClassifier.classify(image.width, image.height)
        offset = int(dhash[:4], 16) % 5

        phrases = {
            "Aesthetic": ["Chasing quiet moments in full color", "A frame where the stillness speaks", "Golden light and gentle horizons", "Moments etched in simplicity", "Filtered only by reality"],
            "Emotional": ["Some memories never lose their warmth", "A chapter worth pausing on", "Carrying this feeling into tomorrow", "The little things that anchor us", "Forever grateful for days like this"],
            "Creative / Trending": ["POV: living inside the aesthetic", "Main character energy, no script needed", "Serving visuals with zero effort", "Core memory officially unlocked", "Vibes louder than words"]
        }

        captions = []
        for style in ["Aesthetic", "Emotional", "Creative / Trending"]:
            pool = phrases.get(style, phrases["Aesthetic"])
            text = pool[(offset + len(captions)) % len(pool)]
            captions.append({
                "style": style,
                "text": text,
                "hashtags": [f"#{category}", f"#{tone}", "#VisionSpeak", "#Photography"]
            })

        return {
            "mode": "deterministic_fallback",
            "dhash": dhash,
            "dominant_colors": colors,
            "composition": comp,
            "captions": captions
        }
