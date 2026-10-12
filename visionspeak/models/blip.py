"""
VisionSpeak Salesforce BLIP Model Integration
=============================================
Pretrained Salesforce BLIP Image Captioning (Base / Large) integration
via Hugging Face Transformers.
Supports local weight caching, offline execution, CPU & CUDA acceleration,
and deterministic beam search or nucleus sampling.

Model License: BSD 3-Clause (Salesforce Research)
Reference: https://huggingface.co/Salesforce/blip-image-captioning-base
"""

import time
import os
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any
from PIL import Image

from visionspeak.models.base import (
    BaseCaptionModel,
    CaptionResult,
    ModelStatus,
    ModelLoadError,
    InferenceError,
)

class BlipCaptionModel(BaseCaptionModel):
    """
    Salesforce BLIP (Bootstrapping Language-Image Pre-training)
    conditional and unconditional caption generator.
    """

    MODEL_ID = "Salesforce/blip-image-captioning-base"
    LICENSE = "BSD-3-Clause (Salesforce)"

    def __init__(
        self,
        model_name: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        device: Optional[Any] = None,
        offline_mode: bool = False
    ):
        self.model_name = model_name or self.MODEL_ID
        self.cache_dir = cache_dir or (Path.home() / ".cache" / "visionspeak" / "models")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.requested_device = device
        self.offline_mode = offline_mode

        self._model = None
        self._processor = None
        self._resolved_device = None
        self._lock = threading.RLock()
        self._load_timestamp: Optional[float] = None

    def _resolve_device(self):
        """Resolve PyTorch device safely."""
        import torch

        if self.requested_device is not None:
            if isinstance(self.requested_device, str):
                if self.requested_device == "cuda" and torch.cuda.is_available():
                    return torch.device("cuda:0")
                elif self.requested_device == "cuda" and not torch.cuda.is_available():
                    raise RuntimeError("CUDA was requested, but no CUDA-enabled GPU is detected.")
                elif self.requested_device == "cpu":
                    return torch.device("cpu")
                else:  # 'auto'
                    return torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
            return self.requested_device

        return torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")

    def is_cached_locally(self) -> bool:
        """Inspect cache directory for existing model snapshots."""
        if not self.cache_dir.exists():
            return False
        # Check for model index or weight files in cache directory
        for root, _, files in os.walk(self.cache_dir):
            for file in files:
                if file.endswith((".bin", ".safetensors", ".h5")) or "snapshots" in root:
                    return True
        return False

    def load(self) -> None:
        """
        Load model and processor from local cache or Hugging Face repository.
        Thread-safe and idempotent.
        """
        with self._lock:
            if self.is_loaded():
                return

            try:
                import torch
                from transformers import BlipProcessor, BlipForConditionalGeneration

                self._resolved_device = self._resolve_device()
                
                # If weights are already cached, load directly from disk without remote network latency
                cached = self.is_cached_locally()
                use_local_only = self.offline_mode or cached

                # Load processor and model using Transformers APIs
                self._processor = BlipProcessor.from_pretrained(
                    self.model_name,
                    cache_dir=str(self.cache_dir),
                    local_files_only=use_local_only
                )

                # Load model weights
                model_kwargs = {"cache_dir": str(self.cache_dir), "local_files_only": use_local_only}
                
                # Use FP16 only if running on CUDA with compute capability >= 7.0
                if self._resolved_device.type == "cuda" and torch.cuda.get_device_capability(0)[0] >= 7:
                    model_kwargs["torch_dtype"] = torch.float16

                self._model = BlipForConditionalGeneration.from_pretrained(
                    self.model_name,
                    **model_kwargs
                )

                self._model.to(self._resolved_device)
                self._model.eval()  # Set evaluation mode
                self._load_timestamp = time.time()

            except ImportError as e:
                raise ModelLoadError(f"Required ML packages (torch, transformers) are missing: {str(e)}")
            except Exception as e:
                self._model = None
                self._processor = None
                raise ModelLoadError(f"Failed to initialize BLIP model ({self.model_name}): {str(e)}")

    def unload(self) -> None:
        """Release loaded model and clean up memory."""
        with self._lock:
            if self._model is not None:
                del self._model
                self._model = None
            if self._processor is not None:
                del self._processor
                self._processor = None

            self._load_timestamp = None

            try:
                import gc
                gc.collect()
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except Exception:
                pass

    def is_loaded(self) -> bool:
        """Verify whether model and processor are initialized in memory."""
        return self._model is not None and self._processor is not None

    def generate(
        self,
        image: Image.Image,
        prompt: Optional[str] = None,
        max_new_tokens: int = 50,
        min_new_tokens: int = 8,
        num_beams: int = 3,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repetition_penalty: float = 1.2,
        do_sample: bool = False,
        style: str = "general"
    ) -> CaptionResult:
        """
        Execute real vision inference on an input PIL image.
        Supports conditioned prefix prompts and parameter tuning.
        """
        if not self.is_loaded():
            self.load()

        import torch

        start_time = time.perf_counter()

        try:
            # Prepare multimodal inputs
            if prompt and prompt.strip():
                clean_prompt = prompt.strip()
                inputs = self._processor(images=image, text=clean_prompt, return_tensors="pt")
            else:
                clean_prompt = None
                inputs = self._processor(images=image, return_tensors="pt")

            # Move inputs to target device
            inputs = {k: v.to(self._resolved_device) for k, v in inputs.items()}

            gen_kwargs: Dict[str, Any] = {
                "max_new_tokens": max(5, min(max_new_tokens, 150)),
                "min_new_tokens": max(2, min_new_tokens),
                "repetition_penalty": max(1.0, repetition_penalty),
            }

            if do_sample:
                gen_kwargs["do_sample"] = True
                gen_kwargs["temperature"] = max(0.1, min(temperature, 1.5))
                gen_kwargs["top_p"] = max(0.1, min(top_p, 1.0))
                gen_kwargs["num_beams"] = 1
            else:
                gen_kwargs["do_sample"] = False
                gen_kwargs["num_beams"] = max(1, min(num_beams, 8))

            # Run PyTorch forward pass without gradient tracking
            with torch.no_grad():
                output_tokens = self._model.generate(**inputs, **gen_kwargs)

            # Decode token IDs to text
            decoded_text = self._processor.decode(output_tokens[0], skip_special_tokens=True).strip()

            # Clean decoded output (capitalize first character, ensure clean punctuation)
            if decoded_text:
                decoded_text = decoded_text[0].upper() + decoded_text[1:]

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            num_tokens = len(output_tokens[0])

            return CaptionResult(
                caption=decoded_text,
                style=style,
                generation_time_ms=round(elapsed_ms, 2),
                model_name=self.model_name,
                device=str(self._resolved_device),
                num_tokens=num_tokens,
                prompt=clean_prompt,
                metadata={
                    "num_beams": gen_kwargs.get("num_beams", 1),
                    "do_sample": do_sample,
                    "max_new_tokens": gen_kwargs["max_new_tokens"]
                }
            )

        except Exception as e:
            raise InferenceError(f"BLIP model inference failed: {str(e)}")

    def status(self) -> ModelStatus:
        """Return real-time operational status."""
        import torch

        mem_mb = None
        if self._resolved_device and self._resolved_device.type == "cuda" and torch.cuda.is_available():
            mem_mb = round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2)

        return ModelStatus(
            model_name=self.model_name,
            is_loaded=self.is_loaded(),
            device=str(self._resolved_device or "uninitialized"),
            cached_locally=self.is_cached_locally(),
            cache_dir=str(self.cache_dir),
            memory_allocated_mb=mem_mb,
            details={
                "license": self.LICENSE,
                "offline_mode": self.offline_mode,
                "uptime_seconds": round(time.time() - self._load_timestamp, 1) if self._load_timestamp else 0
            }
        )
