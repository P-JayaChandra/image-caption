"""
SQLite Database Hot Backup and Vacuum Utility
"""
import sqlite3
import os

class DatabaseBackup:
    @staticmethod
    def backup(source_path: str, target_path: str):
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        with sqlite3.connect(source_path) as src, sqlite3.connect(target_path) as dst:
            src.backup(dst)

    @staticmethod
    def vacuum(db_path: str):
        with sqlite3.connect(db_path) as conn:
            conn.execute("VACUUM")
