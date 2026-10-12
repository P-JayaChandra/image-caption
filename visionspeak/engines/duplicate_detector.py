"""
Near-Duplicate Image Detector Index
"""
from visionspeak.engines.hashing import PerceptualHasher

class DuplicateDetector:
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.index = {}

    def register(self, image_id: str, dhash: str):
        self.index[image_id] = dhash

    def find_match(self, dhash: str):
        for img_id, indexed_hash in self.index.items():
            dist = PerceptualHasher.hamming_distance(dhash, indexed_hash)
            if dist <= self.threshold:
                return {"match": True, "image_id": img_id, "distance": dist}
        return {"match": False}
