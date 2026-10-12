"""
Dominant Color Palette and Mood Extractor
"""
from PIL import Image

class ColorAnalyzer:
    @staticmethod
    def extract_palette(image: Image.Image, num_colors: int = 5):
        small = image.convert("RGB").resize((50, 50))
        colors = small.getcolors(2500)
        if not colors:
            return ["#888888"]
        sorted_colors = sorted(colors, key=lambda c: c[0], reverse=True)[:num_colors]
        hex_palette = [f"#{r:02x}{g:02x}{b:02x}" for count, (r, g, b) in sorted_colors]
        return hex_palette

    @staticmethod
    def classify_temperature(image: Image.Image) -> str:
        small = image.convert("RGB").resize((10, 10))
        pixels = list(small.getdata())
        r_avg = sum(p[0] for p in pixels) / len(pixels)
        b_avg = sum(p[2] for p in pixels) / len(pixels)
        if r_avg > b_avg + 15:
            return "Warm"
        elif b_avg > r_avg + 15:
            return "Cool"
        return "Neutral"
