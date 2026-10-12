"""
VISIONSPEAK — High Performance Local AI Image Captioning Platform
==================================================================
Fully offline-capable multimodal vision captioning powered by Salesforce BLIP.
Zero API keys required.
"""

__version__ = "1.0.0"
__author__ = "P-JayaChandra"
__license__ = "Proprietary"

from visionspeak.config import VisionSpeakConfig, get_config
from visionspeak.device import DeviceManager, get_device_manager
from visionspeak.models.manager import ModelManager, get_model_manager

__all__ = [
    "VisionSpeakConfig",
    "get_config",
    "DeviceManager",
    "get_device_manager",
    "ModelManager",
    "get_model_manager",
    "__version__",
]
