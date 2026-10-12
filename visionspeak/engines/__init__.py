"""
VisionSpeak Engines Subpackage
==============================
Advanced evaluation metrics, perceptual hashing, social media formatting templates,
and multilingual localization pipelines.
"""

from visionspeak.engines.evaluator import CaptionEvaluator, EvaluationReport
from visionspeak.engines.templates import PlatformTemplateManager, SocialPlatform
from visionspeak.engines.multilingual import MultilingualCaptionAdapter, SupportedLanguage
from visionspeak.engines.hashing import PerceptualHasher, DuplicateDetector

__all__ = [
    "CaptionEvaluator",
    "EvaluationReport",
    "PlatformTemplateManager",
    "SocialPlatform",
    "MultilingualCaptionAdapter",
    "SupportedLanguage",
    "PerceptualHasher",
    "DuplicateDetector",
]
