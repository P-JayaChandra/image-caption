"""
VisionSpeak Models Subpackage
=============================
Abstract model interfaces, Salesforce BLIP integration, and model lifecycle management.
"""

from visionspeak.models.base import (
    BaseCaptionModel,
    CaptionResult,
    BatchCaptionResult,
    ModelStatus,
    ModelLoadError,
    InferenceError,
)
from visionspeak.models.blip import BlipCaptionModel
from visionspeak.models.manager import ModelManager, get_model_manager

__all__ = [
    "BaseCaptionModel",
    "CaptionResult",
    "BatchCaptionResult",
    "ModelStatus",
    "ModelLoadError",
    "InferenceError",
    "BlipCaptionModel",
    "ModelManager",
    "get_model_manager",
]
