"""
Platform-Specific Social Media Template Formatting Engine
"""
from enum import Enum
from typing import List, Dict, Any

class SocialPlatform(Enum):
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    PINTEREST = "pinterest"
    TIKTOK = "tiktok"

class PlatformTemplateManager:
    @staticmethod
    def format_instagram(caption: str, hashtags: List[str], cta: str = "Double tap if you agree!") -> str:
        tag_str = " ".join(hashtags)
        return f"{caption}\n.\n.\n{cta}\n.\n{tag_str}"

    @staticmethod
    def format_twitter(caption: str, hashtags: List[str]) -> str:
        tags = " ".join(hashtags[:2])
        full = f"{caption} {tags}".strip()
        return full[:280]

    @staticmethod
    def format_linkedin(caption: str, takeaways: List[str], hashtags: List[str]) -> str:
        points = "\n".join([f"• {t}" for t in takeaways]) if takeaways else ""
        tag_str = " ".join(hashtags[:4])
        return f"{caption}\n\nKey Perspectives:\n{points}\n\n{tag_str}"

    @staticmethod
    def format_tiktok(caption: str, hashtags: List[str]) -> str:
        tags = " ".join(hashtags + ["#fyp", "#viral", "#foryou"])
        return f"Wait for the detail... ✨ {caption} {tags}"
