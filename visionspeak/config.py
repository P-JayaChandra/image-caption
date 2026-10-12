"""
VisionSpeak Configuration Module
================================
Centralized configuration management for model inference, storage,
image upload constraints, and runtime parameters.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class VisionSpeakConfig:
    """Application configuration with sensible local-first defaults."""

    # Project directories
    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    cache_dir: Path = field(default_factory=lambda: Path.home() / ".cache" / "visionspeak" / "models")
    data_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data")
    temp_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent.parent / "temp")

    # AI Model settings
    model_name: str = "Salesforce/blip-image-captioning-base"
    fallback_model_name: str = "Salesforce/blip-image-captioning-base"
    model_revision: str = "main"
    offline_mode: bool = False
    
    # Device configuration: 'auto', 'cpu', or 'cuda'
    device: str = "auto"
    torch_num_threads: int = 4
    enable_half_precision: bool = False  # FP16 for CUDA if supported

    # Image upload and safety constraints
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10 MB
    max_image_dimension: int = 4096
    max_image_pixels: int = 4096 * 4096  # 16 MP to prevent decompression bombs
    allowed_mime_types: List[str] = field(default_factory=lambda: [
        "image/jpeg",
        "image/png",
        "image/webp"
    ])

    # Caption generation defaults
    default_max_new_tokens: int = 50
    default_min_new_tokens: int = 8
    default_num_beams: int = 3
    default_repetition_penalty: float = 1.2
    default_temperature: float = 0.7
    default_top_p: float = 0.9

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    cors_origins: List[str] = field(default_factory=lambda: [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5000",
        "*"
    ])

    # Database
    db_filename: str = "visionspeak.db"

    @property
    def db_path(self) -> Path:
        return self.data_dir / self.db_filename

    @property
    def sqlite_url(self) -> str:
        return f"sqlite:///{self.db_path.as_posix()}"

    def ensure_directories(self) -> None:
        """Create required local directories safely."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

_config_instance: Optional[VisionSpeakConfig] = None

def get_config() -> VisionSpeakConfig:
    """Retrieve or initialize the singleton configuration."""
    global _config_instance
    if _config_instance is None:
        # Load environment overrides
        model_name = os.getenv("BLIP_MODEL_NAME", "Salesforce/blip-image-captioning-base")
        device = os.getenv("AI_DEVICE", "auto")
        port = int(os.getenv("AI_SERVICE_PORT", "8000"))
        threads = int(os.getenv("TORCH_NUM_THREADS", "4"))
        offline = os.getenv("AI_OFFLINE_MODE", "false").lower() in ("1", "true", "yes")

        cache_dir_env = os.getenv("VISION_SPEAK_CACHE_DIR") or os.getenv("MODEL_CACHE_DIR")
        cache_path = Path(cache_dir_env).resolve() if cache_dir_env else (Path.home() / ".cache" / "visionspeak" / "models")

        _config_instance = VisionSpeakConfig(
            cache_dir=cache_path,
            model_name=model_name,
            device=device,
            port=port,
            torch_num_threads=threads,
            offline_mode=offline
        )
        _config_instance.ensure_directories()
    return _config_instance
