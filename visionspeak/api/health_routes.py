"""
Health and Hardware Diagnostics Endpoints
"""
import time
from fastapi import APIRouter
from visionspeak.device import get_device_manager

router = APIRouter(prefix="/api/v1/health", tags=["Health"])
START_TIME = time.time()

@router.get("")
async def health_check():
    dm = get_device_manager()
    return {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "device": dm.device_type,
        "mode": "100% offline local inference",
        "api_keys_required": False
    }
