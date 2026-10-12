"""
LinkedIn Professional Storytelling Adapter
"""

class LinkedInAdapter:
    @staticmethod
    def format(headline: str, narrative: str, takeaways: list = None, hashtags: list = None) -> str:
        body = [f"📸 Visual Focus: {headline}", "", narrative, ""]
        if takeaways:
            body.append("Key Observations:")
            for item in takeaways:
                body.append(f"→ {item}")
            body.append("")
        body.append("What perspective stands out to you? Share your thoughts below.")
        if hashtags:
            body.append("")
            body.append(" ".join([f"#{h.strip('#')}" for h in hashtags[:5]]))
        return "\n".join(body)
