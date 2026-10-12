"""
Lightweight Schema Migration Engine
"""
import sqlite3

class MigrationEngine:
    def __init__(self, db_path: str = "data/visionspeak.db"):
        self.db_path = db_path

    def run_migrations(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor = conn.execute("SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1")
            row = cursor.fetchone()
            current_version = row[0] if row else 0

            if current_version < 1:
                conn.execute("INSERT INTO schema_migrations (version) VALUES (1)")
            conn.commit()
