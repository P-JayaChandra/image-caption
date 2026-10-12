"""
VisionSpeak Base Model Definitions
==================================
Abstract interface, telemetry containers, and exception hierarchies
for local multimodal vision inference.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from PIL import Image

class ModelLoadError(Exception):
    """Raised when model weights cannot be loaded or initialized."""
    pass

class InferenceError(Exception):
    """Raised when inference execution fails."""
    pass

@dataclass
class CaptionResult:
    """Result container for a single generated caption."""
    caption: str
    style: str
    generation_time_ms: float
    model_name: str
    device: str
    num_tokens: int = 0
    prompt: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BatchCaptionResult:
    """Result container for batch inference."""
    results: List[CaptionResult]
    total_time_ms: float
    batch_size: int
    throughput_items_per_sec: float

@dataclass
class ModelStatus:
    """Operational status and health of the vision model."""
    model_name: str
    is_loaded: bool
    device: str
    cached_locally: bool
    cache_dir: str
    memory_allocated_mb: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)

class BaseCaptionModel(ABC):
    """Abstract base class for all vision captioning backends."""

    @abstractmethod
    def load(self) -> None:
        """Load model weights and processor into memory."""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload model from memory to free system resources."""
        pass

    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if model is currently ready in memory."""
        pass

    @abstractmethod
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
        """Generate a caption for a single PIL image."""
        pass

    @abstractmethod
    def status(self) -> ModelStatus:
        """Return the current operational status of the model."""
        pass
