"""
RFC 4180 Compliant CSV Export Formatter
"""
import csv
import io
from typing import List, Dict, Any

class CsvExporter:
    @staticmethod
    def export(records: List[Dict[str, Any]]) -> str:
        output = io.StringIO()
        fieldnames = ["id", "image_name", "style", "caption_text", "hashtags", "created_at"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            row = dict(r)
            if isinstance(row.get("hashtags"), list):
                row["hashtags"] = " ".join(row["hashtags"])
            writer.writerow(row)
        return output.getvalue()
