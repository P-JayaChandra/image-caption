"""
VisionSpeak Image Validation Module
===================================
Robust image security, magic-byte inspection, memory boundary verification,
and decompression bomb mitigation.
"""

import io
from typing import Tuple, Optional
from dataclasses import dataclass
from PIL import Image

class ImageValidationError(Exception):
    """Base exception for all image validation failures."""
    pass

class FileSizeExceededError(ImageValidationError):
    """Uploaded payload exceeds maximum permissible size."""
    pass

class UnsupportedFormatError(ImageValidationError):
    """Uploaded file does not match approved MIME types or image magic bytes."""
    pass

class DecompressionBombError(ImageValidationError):
    """Image dimensions exceed safe limits, threatening system memory."""
    pass

class CorruptedImageError(ImageValidationError):
    """Image data stream cannot be decoded or verified."""
    pass

@dataclass
class ValidatedImageMetadata:
    """Metadata describing a validated image."""
    format: str
    mime_type: str
    width: int
    height: int
    size_bytes: int
    mode: str
    has_alpha: bool

class ImageValidator:
    """Performs defensive validation of image bytes before model preprocessing."""

    # Magic byte signatures
    MAGIC_JPEG = b"\xff\xd8\xff"
    MAGIC_PNG = b"\x89PNG\r\n\x1a\n"
    MAGIC_WEBP_RIFF = b"RIFF"
    MAGIC_WEBP_FOURCC = b"WEBP"

    def __init__(
        self,
        max_size_bytes: int = 10 * 1024 * 1024,
        max_dimension: int = 4096,
        max_pixels: int = 16_000_000
    ):
        self.max_size_bytes = max_size_bytes
        self.max_dimension = max_dimension
        self.max_pixels = max_pixels

    def sniff_mime_type(self, raw_bytes: bytes) -> str:
        """
        Determine actual image MIME type by inspecting leading magic bytes.
        Does NOT rely on untrusted client filenames.
        """
        if len(raw_bytes) < 12:
            raise UnsupportedFormatError("File is too small to contain valid image magic bytes.")

        if raw_bytes.startswith(self.MAGIC_JPEG):
            return "image/jpeg"
        if raw_bytes.startswith(self.MAGIC_PNG):
            return "image/png"
        if raw_bytes.startswith(self.MAGIC_WEBP_RIFF) and raw_bytes[8:12] == self.MAGIC_WEBP_FOURCC:
            return "image/webp"

        raise UnsupportedFormatError(
            "Unsupported file format. Only true JPEG, PNG, and WebP images are permitted."
        )

    def validate(self, raw_bytes: bytes) -> Tuple[Image.Image, ValidatedImageMetadata]:
        """
        Fully validate raw image byte payload.
        Returns a verified, decoded PIL Image and its metadata.
        """
        if not raw_bytes:
            raise ImageValidationError("Empty image payload received.")

        # 1. Payload size verification
        size_bytes = len(raw_bytes)
        if size_bytes > self.max_size_bytes:
            raise FileSizeExceededError(
                f"File size ({size_bytes / (1024 * 1024):.2f} MB) exceeds maximum permitted limit of {self.max_size_bytes / (1024 * 1024):.2f} MB."
            )

        # 2. Magic byte inspection
        mime_type = self.sniff_mime_type(raw_bytes)

        # 3. Configure Pillow decompression bomb protection
        Image.MAX_IMAGE_PIXELS = self.max_pixels

        # 4. Safe image decoding & integrity verification
        try:
            byte_stream = io.BytesIO(raw_bytes)
            img = Image.open(byte_stream)

            # Pillow verify checks format and headers without decoding all pixels
            img.verify()

            # Re-open stream for actual pixel access (since verify closes/invalidates stream)
            byte_stream.seek(0)
            img = Image.open(byte_stream)
            img.load()  # Force decode to catch truncated files or malicious byte streams
        except (Image.DecompressionBombError, ValueError) as e:
            raise DecompressionBombError(
                f"Image dimensions exceed safe limits ({self.max_pixels} pixels): {str(e)}"
            )
        except Exception as e:
            raise CorruptedImageError(f"Corrupted or invalid image stream: {str(e)}")

        width, height = img.size

        # 5. Dimension checks
        if width > self.max_dimension or height > self.max_dimension:
            raise DecompressionBombError(
                f"Image dimensions ({width}x{height}) exceed maximum allowed dimension of {self.max_dimension}px."
            )

        total_pixels = width * height
        if total_pixels > self.max_pixels:
            raise DecompressionBombError(
                f"Total image pixels ({total_pixels}) exceeds safe limit of {self.max_pixels} pixels."
            )

        metadata = ValidatedImageMetadata(
            format=img.format or mime_type.split("/")[-1].upper(),
            mime_type=mime_type,
            width=width,
            height=height,
            size_bytes=size_bytes,
            mode=img.mode,
            has_alpha=("A" in img.mode or img.mode == "RGBA" or "transparency" in img.info)
        )

        return img, metadata
