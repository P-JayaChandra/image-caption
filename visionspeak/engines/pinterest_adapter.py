"""
Pinterest Visual Discovery and Pin Optimizer
"""

class PinterestAdapter:
    @staticmethod
    def format_pin(title: str, description: str, keywords: list = None) -> dict:
        clean_title = title.strip()[:100]
        kw_str = " | ".join(keywords[:5]) if keywords else ""
        clean_desc = f"{description.strip()} Find inspiration: {kw_str}"[:500]
        return {
            "pin_title": clean_title,
            "pin_description": clean_desc,
            "search_keywords": keywords or []
        }
