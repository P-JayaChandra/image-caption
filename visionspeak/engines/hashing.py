"""
Perceptual Hashing and Image Fingerprinting
"""
import hashlib
from PIL import Image

class PerceptualHasher:
    @staticmethod
    def compute_dhash(image: Image.Image, hash_size: int = 8) -> str:
        resized = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        pixels = list(resized.getdata())
        diff = []
        for row in range(hash_size):
            for col in range(hash_size):
                left = pixels[row * (hash_size + 1) + col]
                right = pixels[row * (hash_size + 1) + col + 1]
                diff.append(1 if left > right else 0)
        decimal_val = 0
        hex_str = []
        for i, val in enumerate(diff):
            if val:
                decimal_val += 2 ** (i % 4)
            if i % 4 == 3:
                hex_str.append(hex(decimal_val)[2:])
                decimal_val = 0
        return "".join(hex_str)

    @staticmethod
    def hamming_distance(hash1: str, hash2: str) -> int:
        if len(hash1) != len(hash2):
            return 999
        return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
