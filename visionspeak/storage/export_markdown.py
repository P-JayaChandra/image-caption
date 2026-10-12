"""
Markdown Summary Report Exporter
"""
from typing import List, Dict, Any

class MarkdownExporter:
    @staticmethod
    def export(records: List[Dict[str, Any]]) -> str:
        md = ["# VisionSpeak Caption Export Report", "", "Generated offline via VisionSpeak AI.", ""]
        for i, r in enumerate(records, 1):
            md.append(f"## {i}. {r.get('image_name', 'Untitled Image')}")
            md.append(f"- **Style**: `{r.get('style', 'Aesthetic')}`")
            md.append(f"- **Caption**: > {r.get('caption_text', '')}")
            if r.get('hashtags'):
                tags = " ".join(r['hashtags']) if isinstance(r['hashtags'], list) else r['hashtags']
                md.append(f"- **Hashtags**: `{tags}`")
            md.append("")
        return "\n".join(md)
