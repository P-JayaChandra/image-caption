"""
Intelligent Hashtag Optimizer
"""
import re

class HashtagOptimizer:
    @staticmethod
    def sanitize(tag: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9]", "", tag)
        return f"#{clean}" if clean else "#VisionSpeak"

    @classmethod
    def generate_tags(cls, category: str, mood: str, custom_keywords=None):
        tags = [cls.sanitize(category), cls.sanitize(mood), "#VisualStory", "#ShotOnCamera", "#ExploreMore"]
        if custom_keywords:
            for kw in custom_keywords:
                tags.append(cls.sanitize(kw))
        return list(dict.fromkeys(tags))[:10]
