"""
VisionSpeak Database Models
===========================
Relational persistence schema for generated captions, image metadata,
user edits, and audit logs using SQLAlchemy 2.0.
"""

from datetime import datetime, timezone
import json
from typing import Optional, List
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from visionspeak.config import get_config

Base = declarative_base()

class ImageRecord(Base):
    """Metadata record for an uploaded/processed image."""
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    format = Column(String(32), nullable=False)
    mime_type = Column(String(64), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    captions = relationship("CaptionRecord", back_populates="image", cascade="all, delete-orphan")

class CaptionRecord(Base):
    """Generated caption record with user-editing audit tracking."""
    __tablename__ = "captions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False, index=True)
    style = Column(String(64), nullable=False, index=True)  # Aesthetic, Emotional, Creative, Alt-Text
    generated_text = Column(Text, nullable=False)
    edited_text = Column(Text, nullable=True)
    is_edited = Column(Boolean, default=False, nullable=False)
    hashtags_json = Column(Text, default="[]", nullable=False)
    category = Column(String(64), default="Other", nullable=False, index=True)
    tone = Column(String(64), default="Aesthetic", nullable=False, index=True)
    model_name = Column(String(128), nullable=False)
    device = Column(String(64), nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    image = relationship("ImageRecord", back_populates="captions")

    @property
    def hashtags(self) -> List[str]:
        try:
            return json.loads(self.hashtags_json) if self.hashtags_json else []
        except Exception:
            return []

    @hashtags.setter
    def hashtags(self, tags: List[str]):
        self.hashtags_json = json.dumps(tags)

    @property
    def effective_text(self) -> str:
        """Return user-edited text if edited, otherwise AI-generated text."""
        return self.edited_text if self.is_edited and self.edited_text else self.generated_text

class AuditLog(Base):
    """Audit log tracking system lifecycle events."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(64), nullable=False, index=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

_engine = None
_SessionFactory = None

def get_engine():
    """Singleton database engine configured with SQLite WAL mode."""
    global _engine
    if _engine is None:
        config = get_config()
        config.ensure_directories()
        _engine = create_engine(
            config.sqlite_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
    return _engine

def init_db() -> None:
    """Initialize database tables idempotently."""
    engine = get_engine()
    Base.metadata.create_all(engine)

def get_session() -> Session:
    """Provide a new transactional SQLAlchemy session."""
    global _SessionFactory
    if _SessionFactory is None:
        engine = get_engine()
        _SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return _SessionFactory()
