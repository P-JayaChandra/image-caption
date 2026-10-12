"""
Image Aspect Ratio and Composition Classifier
"""
from PIL import Image

class CompositionClassifier:
    @staticmethod
    def classify(width: int, height: int):
        ratio = round(width / height, 2)
        if 0.95 <= ratio <= 1.05:
            orientation = "Square (1:1)"
            target = "Instagram Feed / Carousel"
        elif ratio < 0.95:
            orientation = "Portrait (4:5 or 9:16)"
            target = "Instagram Reels / Stories / TikTok"
        else:
            orientation = "Landscape (16:9 or 3:2)"
            target = "X / Twitter / LinkedIn / YouTube"
        return {
            "aspect_ratio": ratio,
            "orientation": orientation,
            "recommended_platform": target
        }
