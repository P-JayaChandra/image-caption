"""
Plain Text Social Clipboard Formatter
"""
from typing import List, Dict, Any

class TextExporter:
    @staticmethod
    def export(records: List[Dict[str, Any]]) -> str:
        lines = []
        for r in records:
            lines.append(r.get("caption_text", "").strip())
            tags = r.get("hashtags", "")
            if isinstance(tags, list):
                tags = " ".join(tags)
            if tags:
                lines.append(f"\n{tags.strip()}\n")
            lines.append("-" * 40)
        return "\n".join(lines)
