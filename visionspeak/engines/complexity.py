"""
Visual Edge Density and Scene Complexity Estimator
"""
from PIL import Image, ImageFilter

class VisualComplexityEstimator:
    @staticmethod
    def estimate(image: Image.Image) -> dict:
        gray = image.convert("L").resize((100, 100))
        edges = gray.filter(ImageFilter.FIND_EDGES)
        pixels = list(edges.getdata())
        edge_sum = sum(p for p in pixels if p > 50)
        max_possible = len(pixels) * 255
        score = round(edge_sum / max_possible, 3)
        return {
            "complexity_score": score,
            "scene_style": "Minimalist" if score < 0.15 else "Intricate / Detailed"
        }
