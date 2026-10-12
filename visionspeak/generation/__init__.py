"""
VisionSpeak Generation Subpackage
=================================
Multi-style Instagram caption generation, visual analysis synthesis,
and accessibility alt-text formatting.
"""

from visionspeak.generation.caption_generator import (
    CaptionGenerator,
    MultiStyleCaptionOutput,
    StyledCaptionItem,
)

__all__ = [
    "CaptionGenerator",
    "MultiStyleCaptionOutput",
    "StyledCaptionItem",
]
