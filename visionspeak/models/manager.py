"""
VisionSpeak Model Lifecycle Manager
===================================
Singleton controller orchestrating model initialization, lazy-loading,
pre-warming, and device resource coordination.
"""

import threading
from typing import Optional, Dict, Any
from pathlib import Path

from visionspeak.config import get_config
from visionspeak.device import get_device_manager
from visionspeak.models.base import BaseCaptionModel, ModelStatus
from visionspeak.models.blip import BlipCaptionModel

class ModelManager:
    """Orchestrates model lifecycle, memory allocation, and singleton availability."""

    def __init__(self):
        self._lock = threading.RLock()
        self._active_model: Optional[BaseCaptionModel] = None
        self._active_model_name: Optional[str] = None

    def get_model(self, model_name: Optional[str] = None, auto_load: bool = True) -> BaseCaptionModel:
        """
        Retrieve or initialize the active captioning model.
        Thread-safe singleton with lazy instantiation.
        """
        with self._lock:
            config = get_config()
            target_name = model_name or config.model_name

            # If model is already instantiated with the same name, return it
            if self._active_model is not None and self._active_model_name == target_name:
                if auto_load and not self._active_model.is_loaded():
                    self._active_model.load()
                return self._active_model

            # If switching models, unload current first
            if self._active_model is not None:
                self._active_model.unload()

            device_mgr = get_device_manager(requested_device=config.device, num_threads=config.torch_num_threads)
            resolved_device = device_mgr.get_device()

            # Instantiate BLIP caption model
            blip_model = BlipCaptionModel(
                model_name=target_name,
                cache_dir=config.cache_dir,
                device=resolved_device,
                offline_mode=config.offline_mode
            )

            if auto_load:
                blip_model.load()

            self._active_model = blip_model
            self._active_model_name = target_name
            return self._active_model

    def unload_model(self) -> None:
        """Explicitly release model from memory."""
        with self._lock:
            if self._active_model is not None:
                self._active_model.unload()
                self._active_model = None
                self._active_model_name = None

    def warmup(self) -> None:
        """Pre-warm the model with a blank synthetic image to eliminate first-request latency."""
        from PIL import Image

        model = self.get_model(auto_load=True)
        # Create a tiny 64x64 synthetic image for warm-up
        dummy_img = Image.new("RGB", (64, 64), color=(200, 200, 200))
        model.generate(dummy_img, max_new_tokens=5, num_beams=1)

    def get_status(self) -> Dict[str, Any]:
        """Aggregate health status from model and hardware manager."""
        config = get_config()
        device_mgr = get_device_manager(requested_device=config.device, num_threads=config.torch_num_threads)
        device_diag = device_mgr.get_diagnostics()

        with self._lock:
            if self._active_model is not None:
                model_status = self._active_model.status()
                status_dict = {
                    "is_loaded": model_status.is_loaded,
                    "model_name": model_status.model_name,
                    "cached_locally": model_status.cached_locally,
                    "cache_dir": model_status.cache_dir,
                    "memory_allocated_mb": model_status.memory_allocated_mb,
                    "details": model_status.details,
                }
            else:
                status_dict = {
                    "is_loaded": False,
                    "model_name": config.model_name,
                    "cached_locally": (config.cache_dir.exists() and any(config.cache_dir.iterdir())),
                    "cache_dir": str(config.cache_dir),
                    "memory_allocated_mb": None,
                    "details": {"offline_mode": config.offline_mode},
                }

        return {
            "model": status_dict,
            "device": device_diag,
            "config": {
                "max_upload_size_mb": config.max_upload_size_bytes / (1024 * 1024),
                "allowed_mime_types": config.allowed_mime_types,
                "torch_num_threads": config.torch_num_threads,
            }
        }

_model_manager_instance: Optional[ModelManager] = None

def get_model_manager() -> ModelManager:
    """Singleton getter for ModelManager."""
    global _model_manager_instance
    if _model_manager_instance is None:
        _model_manager_instance = ModelManager()
    return _model_manager_instance
