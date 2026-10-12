"""
VisionSpeak Image Preprocessor Module
=====================================
Color space normalization, EXIF orientation correction, alpha compositing,
and aspect-ratio preserving resizing for vision transformer input.
"""

from typing import Tuple, Optional
from PIL import Image, ImageOps

class ImagePreprocessor:
    """Prepares validated images for optimal Vision Transformer (BLIP) inference."""

    @staticmethod
    def fix_orientation(image: Image.Image) -> Image.Image:
        """
        Apply EXIF orientation transposition if orientation tags are present.
        Ensures portrait and inverted camera shots are oriented right side up.
        """
        try:
            return ImageOps.exif_transpose(image) or image
        except Exception:
            return image

    @staticmethod
    def to_rgb(image: Image.Image, bg_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """
        Normalize any image mode (RGBA, LA, P, CMYK, L) to standard 3-channel RGB.
        Composites transparent layers over a clean background to prevent visual artifacts.
        """
        if image.mode == "RGB":
            return image

        if image.mode in ("RGBA", "LA") or ("transparency" in image.info):
            # Alpha composite onto solid background
            rgba_img = image.convert("RGBA")
            background = Image.new("RGBA", rgba_img.size, (*bg_color, 255))
            composite = Image.alpha_composite(background, rgba_img)
            return composite.convert("RGB")

        if image.mode == "CMYK":
            return image.convert("RGB")

        if image.mode == "P":
            # Palette mode
            rgba = image.convert("RGBA")
            background = Image.new("RGBA", rgba.size, (*bg_color, 255))
            composite = Image.alpha_composite(background, rgba)
            return composite.convert("RGB")

        # Grayscale 'L' or other single-channel modes
        return image.convert("RGB")

    @classmethod
    def preprocess_for_model(
        cls,
        image: Image.Image,
        target_max_side: Optional[int] = 1024
    ) -> Image.Image:
        """
        Full preprocessing pipeline for model inference:
        1. Correct EXIF orientation.
        2. Normalize mode to clean RGB.
        3. Constrain maximum dimension while preserving aspect ratio.
        """
        img = cls.fix_orientation(image)
        img = cls.to_rgb(img)

        if target_max_side and max(img.size) > target_max_side:
            img.thumbnail((target_max_side, target_max_side), Image.Resampling.LANCZOS)

        return img

    @staticmethod
    def generate_thumbnail(image: Image.Image, size: Tuple[int, int] = (384, 384)) -> Image.Image:
        """Create a scaled down thumbnail for UI preview or caching."""
        thumb = image.copy()
        thumb.thumbnail(size, Image.Resampling.LANCZOS)
        return thumb
