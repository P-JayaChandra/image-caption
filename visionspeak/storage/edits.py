"""
Caption Edit Auditing and Version Tracking Service
"""
import sqlite3
from typing import Optional, List, Dict, Any

class CaptionAuditService:
    def __init__(self, db_path: str = "data/visionspeak.db"):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS caption_edits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    caption_id INTEGER NOT NULL,
                    original_text TEXT NOT NULL,
                    edited_text TEXT NOT NULL,
                    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def record_edit(self, caption_id: int, original: str, edited: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO caption_edits (caption_id, original_text, edited_text) VALUES (?, ?, ?)",
                (caption_id, original, edited)
            )

    def get_history(self, caption_id: int) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM caption_edits WHERE caption_id = ? ORDER BY modified_at DESC",
                (caption_id,)
            )
            return [dict(r) for r in cursor.fetchall()]
