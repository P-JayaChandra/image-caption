"""
Export Endpoints for Captions
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/api/v1/export", tags=["Export"])

@router.get("/{export_format}")
async def export_captions(export_format: str):
    valid = ["json", "csv", "txt", "md"]
    if export_format not in valid:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Choose from {valid}")
    return PlainTextResponse(f"VisionSpeak Export ({export_format})\nStatus: Ready")
