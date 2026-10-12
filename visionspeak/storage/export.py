"""
VisionSpeak Caption Exporter
============================
Multi-format exporter supporting JSON, CSV, and formatted TXT outputs
for single captions or bulk history downloads.
"""

import csv
import io
import json
from enum import Enum
from typing import List, Dict, Any

class ExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    TXT = "txt"

class CaptionExporter:
    """Serializes caption records into standard export formats."""

    @staticmethod
    def to_json(records: List[Dict[str, Any]], indent: int = 2) -> str:
        """Serialize records to formatted JSON."""
        return json.dumps(records, indent=indent, ensure_ascii=False)

    @staticmethod
    def to_csv(records: List[Dict[str, Any]]) -> str:
        """Serialize records to tabular CSV."""
        if not records:
            return ""

        output = io.StringIO()
        fieldnames = [
            "id",
            "filename",
            "style",
            "effective_text",
            "is_edited",
            "generated_text",
            "edited_text",
            "hashtags",
            "category",
            "tone",
            "model_name",
            "device",
            "created_at"
        ]

        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for r in records:
            row = dict(r)
            if isinstance(row.get("hashtags"), list):
                row["hashtags"] = " ".join(row["hashtags"])
            writer.writerow(row)

        return output.getvalue()

    @staticmethod
    def to_txt(records: List[Dict[str, Any]]) -> str:
        """Serialize records to human-readable plain text report."""
        lines = [
            "=" * 70,
            "  VISIONSPEAK — EXPORTED CAPTION ARCHIVE",
            f"  Total Records: {len(records)}",
            "=" * 70,
            ""
        ]

        for i, r in enumerate(records, 1):
            lines.append(f"[{i}] {r.get('filename', 'Unknown')} — Style: {r.get('style', 'General')}")
            lines.append(f"    Category: {r.get('category', 'Other')} | Tone: {r.get('tone', 'Aesthetic')}")
            lines.append(f"    Date: {r.get('created_at', '')}")
            
            caption_text = r.get("effective_text") or r.get("generated_text", "")
            lines.append(f"    Caption: \"{caption_text}\"")
            
            tags = r.get("hashtags", [])
            if isinstance(tags, list) and tags:
                lines.append(f"    Hashtags: {' '.join(tags)}")
            
            if r.get("is_edited"):
                lines.append(f"    (User Modified from original: \"{r.get('generated_text')}\")")

            lines.append("-" * 70)

        return "\n".join(lines)

    @classmethod
    def export(cls, records: List[Dict[str, Any]], fmt: ExportFormat) -> tuple[str, str, str]:
        """
        Export records according to requested format.
        Returns (content_string, mime_type, file_extension).
        """
        if fmt == ExportFormat.CSV:
            return cls.to_csv(records), "text/csv", "csv"
        elif fmt == ExportFormat.TXT:
            return cls.to_txt(records), "text/plain", "txt"
        else:
            return cls.to_json(records), "application/json", "json"

