"""
Caption Styler and Formatting Engine
"""

EMOJI_SETS = {
    "Aesthetic": ["✨", "📸", "🤍"],
    "Emotional": ["🌿", "🌙", "💭"],
    "Creative / Trending": ["⚡", "💫", "🔥"]
}

def style_caption(text: str, style_name: str) -> str:
    cleaned = text.strip().rstrip(".")
    emojis = " ".join(EMOJI_SETS.get(style_name, ["✨"]))
    if style_name == "Aesthetic":
        return f"{cleaned.capitalize()} · {emojis}"
    elif style_name == "Emotional":
        return f"{cleaned.capitalize()} — {emojis}"
    else:
        return f"{cleaned.upper()} // {emojis}"
