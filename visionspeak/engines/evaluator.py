"""
Caption Quality, Readability, and Platform Limit Evaluator
"""

class CaptionEvaluator:
    @staticmethod
    def evaluate(caption_text: str, hashtags: list = None) -> dict:
        char_count = len(caption_text)
        words = caption_text.split()
        word_count = len(words)
        tag_count = len(hashtags) if hashtags else 0

        # Estimated engagement rating
        score = 85
        if 50 <= char_count <= 150:
            score += 10
        if 3 <= tag_count <= 8:
            score += 5

        return {
            "char_count": char_count,
            "word_count": word_count,
            "hashtag_count": tag_count,
            "engagement_score": min(100, score),
            "fits_x_limit": (char_count + tag_count * 15) <= 280,
            "fits_instagram_limit": char_count <= 2200
        }
