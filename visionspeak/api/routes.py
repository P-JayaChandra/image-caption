"""
VisionSpeak REST API Endpoints
==============================
High-performance REST API routing with automatic validation, defensive image handling,
local BLIP inference, database persistence, and multi-format export.
"""

from typing import Optional, List
from fastapi import APIRouter, File, UploadFile, Form, Query, HTTPException, Response, status
from fastapi.responses import PlainTextResponse

from visionspeak.config import get_config
from visionspeak.models.manager import get_model_manager
from visionspeak.processing.image_validator import (
    ImageValidator,
    ImageValidationError,
    FileSizeExceededError,
    UnsupportedFormatError,
    DecompressionBombError,
    CorruptedImageError,
)
from visionspeak.processing.preprocessor import ImagePreprocessor
from visionspeak.generation.caption_generator import CaptionGenerator
from visionspeak.storage.repository import CaptionRepository
from visionspeak.storage.export import ExportFormat, CaptionExporter

router = APIRouter(prefix="/api", tags=["VisionSpeak AI"])

validator = ImageValidator()
repository = CaptionRepository()

@router.get("/health")
async def health_check():
    """
    Comprehensive health check reporting local model status,
    hardware diagnostics, database metrics, and offline readiness.
    """
    model_mgr = get_model_manager()
    status_data = model_mgr.get_status()
    db_metrics = repository.get_metrics()

    return {
        "status": "ok",
        "service": "VisionSpeak Local AI Platform",
        "model": status_data["model"],
        "device": status_data["device"],
        "metrics": db_metrics,
        "offline_ready": status_data["model"]["cached_locally"],
        "cloud_keys_required": False
    }

@router.post("/generate-captions")
async def generate_captions(
    image: UploadFile = File(...),
    category: Optional[str] = Form("Other"),
    tone: Optional[str] = Form("Aesthetic")
):
    """
    Primary image caption generation endpoint.
    Processes uploaded image with local Salesforce BLIP model.
    Zero external API calls.
    """
    try:
        raw_bytes = await image.read()
        if not raw_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty image payload received. Please upload a valid image."
            )

        # Defensive validation (magic bytes, size, decompression bomb mitigation)
        pil_img, metadata = validator.validate(raw_bytes)

        # Preprocess image (EXIF rotation correction, RGB mode normalization)
        preprocessed = ImagePreprocessor.preprocess_for_model(pil_img)

        # Retrieve singleton model and run multi-style caption generation
        model_mgr = get_model_manager()
        model = model_mgr.get_model(auto_load=True)
        generator = CaptionGenerator(model)

        output = generator.generate_all_styles(
            image=preprocessed,
            category=category or "Other",
            tone=tone or "Aesthetic"
        )

        # Persist results to SQLite database
        filename = image.filename or "uploaded_image.jpg"
        repository.save_generation(
            image_meta=metadata,
            filename=filename,
            output=output,
            category=category or "Other",
            tone=tone or "Aesthetic"
        )

        # Return frontend-compatible JSON response
        return {
            "success": True,
            "filename": filename,
            "fileSize": metadata.size_bytes,
            "mimeType": metadata.mime_type,
            "category": category,
            "tone": tone,
            "analysis": {
                "description": output.description,
                "tags": output.tags
            },
            "captions": output.captions,
            "alt_text": output.alt_text,
            "isRealAi": True,
            "model_name": output.model_name,
            "device": output.device,
            "latency_ms": output.total_latency_ms
        }

    except FileSizeExceededError as e:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(e))
    except (UnsupportedFormatError, DecompressionBombError, CorruptedImageError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ImageValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inference error: {str(e)}")

@router.get("/history")
async def get_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    tone: Optional[str] = Query(None),
    style: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    is_edited: Optional[bool] = Query(None)
):
    """Retrieve paginated caption history with search and category filtering."""
    records, total = repository.get_history(
        page=page,
        per_page=per_page,
        category=category,
        tone=tone,
        style=style,
        search_query=search,
        is_edited=is_edited
    )

    return {
        "success": True,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": max(1, (total + per_page - 1) // per_page),
        "items": records
    }

@router.post("/history/{caption_id}/edit")
async def edit_caption(caption_id: int, new_text: str = Form(...)):
    """Record user edits on a generated caption, preserving original AI text."""
    updated = repository.update_caption(caption_id, new_text)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caption record not found.")

    return {
        "success": True,
        "item": updated
    }

@router.delete("/history/{caption_id}")
async def delete_caption(caption_id: int):
    """Delete a caption record from persistence."""
    deleted = repository.delete_caption(caption_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caption record not found.")

    return {"success": True, "message": "Caption deleted successfully."}

@router.get("/export")
async def export_captions(
    format: ExportFormat = Query(ExportFormat.JSON),
    category: Optional[str] = Query(None),
    tone: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Export caption history in JSON, CSV, or TXT format."""
    records, _ = repository.get_history(
        page=1,
        per_page=500,
        category=category,
        tone=tone,
        search_query=search
    )

    content, mime_type, ext = CaptionExporter.export(records, format)
    
    filename = f"visionspeak_captions.{ext}"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}

    return Response(content=content, media_type=mime_type, headers=headers)

@router.post("/caption/batch")
async def batch_caption(
    images: List[UploadFile] = File(...),
    category: Optional[str] = Form("Other"),
    tone: Optional[str] = Form("Aesthetic")
):
    """Batch process multiple images with local BLIP model."""
    if len(images) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 images allowed per batch request."
        )

    model_mgr = get_model_manager()
    model = model_mgr.get_model(auto_load=True)
    generator = CaptionGenerator(model)

    results = []
    for img_file in images:
        try:
            raw_bytes = await img_file.read()
            pil_img, metadata = validator.validate(raw_bytes)
            preprocessed = ImagePreprocessor.preprocess_for_model(pil_img)
            
            output = generator.generate_all_styles(
                image=preprocessed,
                category=category or "Other",
                tone=tone or "Aesthetic"
            )

            repository.save_generation(
                image_meta=metadata,
                filename=img_file.filename or "batch_image.jpg",
                output=output,
                category=category or "Other",
                tone=tone or "Aesthetic"
            )

            results.append({
                "filename": img_file.filename,
                "success": True,
                "analysis": {"description": output.description, "tags": output.tags},
                "captions": output.captions,
                "latency_ms": output.total_latency_ms
            })
        except Exception as e:
            results.append({
                "filename": img_file.filename,
                "success": False,
                "error": str(e)
            })

    return {
        "success": True,
        "batch_size": len(images),
        "results": results
    }

@router.post("/benchmark")
async def benchmark_inference():
    """Run an automated local inference benchmark on a synthetic test image."""
    import time
    from PIL import Image

    model_mgr = get_model_manager()
    model = model_mgr.get_model(auto_load=True)

    # Synthetic test image
    test_img = Image.new("RGB", (384, 384), color=(120, 150, 180))

    runs = 3
    latencies = []

    for _ in range(runs):
        start = time.perf_counter()
        res = model.generate(test_img, max_new_tokens=25, num_beams=1)
        latencies.append((time.perf_counter() - start) * 1000.0)

    avg_ms = round(sum(latencies) / len(latencies), 2)
    min_ms = round(min(latencies), 2)
    max_ms = round(max(latencies), 2)

    return {
        "success": True,
        "model_name": model.status().model_name,
        "device": model.status().device,
        "runs": runs,
        "average_latency_ms": avg_ms,
        "min_latency_ms": min_ms,
        "max_latency_ms": max_ms,
        "throughput_images_per_second": round(1000.0 / avg_ms, 2)
    }
