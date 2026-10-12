"""
VisionSpeak Storage Repository
==============================
CRUD operations, search filters, pagination, and user editing audit history.
"""

from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import or_, desc, asc, func
from sqlalchemy.orm import Session

from visionspeak.storage.database import (
    ImageRecord,
    CaptionRecord,
    AuditLog,
    get_session,
    init_db,
)
from visionspeak.generation.caption_generator import MultiStyleCaptionOutput
from visionspeak.processing.image_validator import ValidatedImageMetadata

class CaptionRepository:
    """Encapsulates data access and transaction boundaries."""

    def __init__(self, session: Optional[Session] = None):
        self._external_session = session
        init_db()

    def _get_session(self) -> Session:
        return self._external_session if self._external_session else get_session()

    def save_generation(
        self,
        image_meta: ValidatedImageMetadata,
        filename: str,
        output: MultiStyleCaptionOutput,
        category: str = "Other",
        tone: str = "Aesthetic"
    ) -> ImageRecord:
        """Atomically persist image metadata and all generated caption variants."""
        session = self._get_session()
        owns_session = self._external_session is None

        try:
            image_record = ImageRecord(
                filename=filename,
                format=image_meta.format,
                mime_type=image_meta.mime_type,
                width=image_meta.width,
                height=image_meta.height,
                size_bytes=image_meta.size_bytes
            )
            session.add(image_record)
            session.flush()  # Obtain generated image_record.id

            # Save the 3 styled captions
            for item in output.captions:
                caption_rec = CaptionRecord(
                    image_id=image_record.id,
                    style=item.get("style", "Aesthetic"),
                    generated_text=item.get("text", ""),
                    category=category,
                    tone=tone,
                    model_name=output.model_name,
                    device=output.device,
                    latency_ms=output.total_latency_ms
                )
                caption_rec.hashtags = item.get("hashtags", [])
                session.add(caption_rec)

            # Also persist accessibility Alt-Text
            if output.alt_text:
                alt_rec = CaptionRecord(
                    image_id=image_record.id,
                    style="Alt-Text",
                    generated_text=output.alt_text,
                    category=category,
                    tone=tone,
                    model_name=output.model_name,
                    device=output.device,
                    latency_ms=output.total_latency_ms
                )
                alt_rec.hashtags = []
                session.add(alt_rec)

            # Audit log
            session.add(AuditLog(
                event_type="GENERATE_CAPTIONS",
                details=f"Generated {len(output.captions)} captions for '{filename}' ({output.total_latency_ms}ms)"
            ))

            if owns_session:
                session.commit()
                session.refresh(image_record)
                image_id = image_record.id

            return image_record

        except Exception:
            if owns_session:
                session.rollback()
            raise
        finally:
            if owns_session:
                session.close()

    def get_history(
        self,
        page: int = 1,
        per_page: int = 20,
        category: Optional[str] = None,
        tone: Optional[str] = None,
        style: Optional[str] = None,
        search_query: Optional[str] = None,
        is_edited: Optional[bool] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Query captions with pagination, search, and category filtering.
        Returns (list_of_records, total_count).
        """
        session = self._get_session()
        owns_session = self._external_session is None

        try:
            query = session.query(CaptionRecord).join(ImageRecord)

            if category and category.lower() != "all":
                query = query.filter(CaptionRecord.category.ilike(category))

            if tone and tone.lower() != "all":
                query = query.filter(CaptionRecord.tone.ilike(tone))

            if style and style.lower() != "all":
                query = query.filter(CaptionRecord.style.ilike(style))

            if is_edited is not None:
                query = query.filter(CaptionRecord.is_edited == is_edited)

            if search_query and search_query.strip():
                term = f"%{search_query.strip()}%"
                query = query.filter(
                    or_(
                        CaptionRecord.generated_text.ilike(term),
                        CaptionRecord.edited_text.ilike(term),
                        ImageRecord.filename.ilike(term),
                        CaptionRecord.hashtags_json.ilike(term)
                    )
                )

            total_count = query.count()

            # Order by latest created
            offset = max(0, (page - 1) * per_page)
            records = query.order_by(desc(CaptionRecord.created_at)).offset(offset).limit(per_page).all()

            results = []
            for r in records:
                results.append({
                    "id": r.id,
                    "image_id": r.image_id,
                    "filename": r.image.filename,
                    "style": r.style,
                    "generated_text": r.generated_text,
                    "edited_text": r.edited_text,
                    "is_edited": r.is_edited,
                    "effective_text": r.effective_text,
                    "hashtags": r.hashtags,
                    "category": r.category,
                    "tone": r.tone,
                    "model_name": r.model_name,
                    "device": r.device,
                    "latency_ms": r.latency_ms,
                    "created_at": r.created_at.isoformat(),
                    "updated_at": r.updated_at.isoformat()
                })

            return results, total_count

        finally:
            if owns_session:
                session.close()

    def update_caption(self, caption_id: int, new_text: str) -> Optional[Dict[str, Any]]:
        """
        Record user-edited caption text.
        Marks `is_edited=True` and records an audit event.
        """
        session = self._get_session()
        owns_session = self._external_session is None

        try:
            record = session.query(CaptionRecord).filter(CaptionRecord.id == caption_id).first()
            if not record:
                return None

            record.edited_text = new_text.strip()
            record.is_edited = True

            session.add(AuditLog(
                event_type="EDIT_CAPTION",
                details=f"User modified caption #{caption_id}"
            ))

            if owns_session:
                session.commit()

            return {
                "id": record.id,
                "style": record.style,
                "generated_text": record.generated_text,
                "edited_text": record.edited_text,
                "is_edited": record.is_edited,
                "effective_text": record.effective_text,
                "hashtags": record.hashtags,
                "updated_at": record.updated_at.isoformat()
            }

        except Exception:
            if owns_session:
                session.rollback()
            raise
        finally:
            if owns_session:
                session.close()

    def delete_caption(self, caption_id: int) -> bool:
        """Delete a single caption record."""
        session = self._get_session()
        owns_session = self._external_session is None

        try:
            record = session.query(CaptionRecord).filter(CaptionRecord.id == caption_id).first()
            if not record:
                return False

            session.delete(record)
            if owns_session:
                session.commit()
            return True
        except Exception:
            if owns_session:
                session.rollback()
            raise
        finally:
            if owns_session:
                session.close()

    def get_metrics(self) -> Dict[str, Any]:
        """Aggregate statistical metrics for diagnostics and dashboards."""
        session = self._get_session()
        owns_session = self._external_session is None

        try:
            total_images = session.query(func.count(ImageRecord.id)).scalar() or 0
            total_captions = session.query(func.count(CaptionRecord.id)).scalar() or 0
            total_edited = session.query(func.count(CaptionRecord.id)).filter(CaptionRecord.is_edited == True).scalar() or 0
            avg_latency = session.query(func.avg(CaptionRecord.latency_ms)).scalar() or 0.0

            return {
                "total_images_processed": total_images,
                "total_captions_generated": total_captions,
                "total_user_edited": total_edited,
                "average_latency_ms": round(float(avg_latency), 2),
            }
        finally:
            if owns_session:
                session.close()
