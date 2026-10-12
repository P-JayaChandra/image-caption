"""
VisionSpeak Hardware & Device Management Module
===============================================
Handles automatic device discovery (CPU / CUDA), hardware diagnostics,
CPU thread optimization, and VRAM management.
"""

import os
import platform
from typing import Dict, Any, Optional

class DeviceManager:
    """Manages computation device resolution and resource allocation."""

    def __init__(self, requested_device: str = "auto", num_threads: int = 4):
        self.requested_device = requested_device.lower().strip()
        self.num_threads = max(1, num_threads)
        self._cached_device = None

    def get_device(self):
        """
        Resolve and return the appropriate PyTorch device.
        Supports 'auto', 'cpu', and 'cuda'.
        """
        import torch

        if self._cached_device is not None:
            return self._cached_device

        if self.requested_device == "cpu":
            target = torch.device("cpu")
        elif self.requested_device == "cuda":
            if torch.cuda.is_available():
                target = torch.device("cuda:0")
            else:
                raise RuntimeError(
                    "CUDA device was explicitly requested, but no compatible CUDA GPU is available on this system."
                )
        else:  # 'auto'
            if torch.cuda.is_available():
                target = torch.device("cuda:0")
            else:
                target = torch.device("cpu")

        # Configure CPU thread count for predictable latency and responsiveness
        if target.type == "cpu":
            try:
                torch.set_num_threads(self.num_threads)
            except Exception:
                pass

        self._cached_device = target
        return self._cached_device

    def get_diagnostics(self) -> Dict[str, Any]:
        """Return system and device diagnostic telemetry."""
        diagnostics: Dict[str, Any] = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
            "requested_device": self.requested_device,
        }

        try:
            import torch
            diagnostics["torch_version"] = torch.__version__
            cuda_avail = torch.cuda.is_available()
            diagnostics["cuda_available"] = cuda_avail

            if cuda_avail:
                diagnostics["cuda_device_count"] = torch.cuda.device_count()
                diagnostics["cuda_device_name"] = torch.cuda.get_device_name(0)
                diagnostics["cuda_capability"] = torch.cuda.get_device_capability(0)
                diagnostics["cuda_memory_allocated_mb"] = round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2)
                diagnostics["cuda_memory_reserved_mb"] = round(torch.cuda.memory_reserved(0) / (1024 * 1024), 2)
            else:
                diagnostics["cuda_device_count"] = 0
                diagnostics["cuda_device_name"] = None

            device = self.get_device()
            diagnostics["active_device"] = str(device)
            diagnostics["active_device_type"] = device.type
            diagnostics["cpu_threads"] = torch.get_num_threads()

        except ImportError:
            diagnostics["torch_version"] = "Not Installed"
            diagnostics["cuda_available"] = False
            diagnostics["active_device"] = "unresolved (torch missing)"

        return diagnostics

    def clear_cache(self) -> None:
        """Free VRAM on CUDA if applicable."""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

_device_manager: Optional[DeviceManager] = None

def get_device_manager(requested_device: str = "auto", num_threads: int = 4) -> DeviceManager:
    """Singleton getter for DeviceManager."""
    global _device_manager
    if _device_manager is None:
        _device_manager = DeviceManager(requested_device=requested_device, num_threads=num_threads)
    return _device_manager
