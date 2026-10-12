"""
TikTok Viral Hook and Cover Title Adapter
"""

HOOKS = [
    "You won't believe how this looks in motion...",
    "POV: When the aesthetic hits just right ✨",
    "Stop scrolling if you love this vibe 📸",
    "Here is the visual story you needed today 👇"
]

class TikTokAdapter:
    @staticmethod
    def format_post(caption: str, category: str = "Aesthetic") -> dict:
        return {
            "cover_hook": HOOKS[0],
            "caption": f"{caption} #visuals #fyp #aesthetic",
            "audio_vibe": "Chill lofi or ambient instrumental"
        }
