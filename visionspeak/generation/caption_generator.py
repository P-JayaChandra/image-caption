"""
VisionSpeak Multi-Style Caption Generator
=========================================
Synthesizes visually-grounded Instagram captions (Aesthetic, Emotional,
Creative / Trending), visual description summaries, tag extraction,
and accessibility alt-text.
"""

import re
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from PIL import Image

from visionspeak.models.base import BaseCaptionModel

@dataclass
class StyledCaptionItem:
    """Single styled caption entry matching frontend expectations."""
    id: int
    style: str
    text: str
    hashtags: List[str]

@dataclass
class MultiStyleCaptionOutput:
    """Aggregated output payload containing visual analysis and 3 captions."""
    description: str
    tags: List[str]
    captions: List[Dict[str, Any]]
    alt_text: str
    isRealAi: bool
    device: str
    total_latency_ms: float
    model_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class CaptionGenerator:
    """Generates multi-perspective captions grounded in visual model predictions."""

    # Curated contextual emoji banks
    CATEGORY_EMOJIS = {
        "Nature": ["🌿", "🍃", "🌲", "🌻", "☀️", "🌊"],
        "People": ["✨", "💫", "🤍", "📸", "🕊️"],
        "Travel": ["✈️", "🗺️", "🌄", "🧭", "🎒", "🌴"],
        "Food": ["☕", "🥐", "🍰", "🍕", "🥂", "🍽️"],
        "Architecture": ["🏛️", "🏢", "📐", "🌆", "✨"],
        "Urban": ["🏙️", "🚦", "🌆", "⚡", "🌃"],
        "Other": ["✨", "📸", "🤍", "💫", "🌟"]
    }

    # Style phrasing templates
    STYLE_TEMPLATES = {
        "Aesthetic": [
            "Whispers of light and texture: {caption}.",
            "Visual poetry in every detail: {caption}.",
            "Finding beauty in simple spaces — {caption}.",
            "Framed in stillness: {caption}."
        ],
        "Emotional": [
            "Moments that quietly stay with you forever — {caption}.",
            "Holding onto feelings words can barely reach: {caption}.",
            "A gentle reminder of what matters: {caption}.",
            "Some memories live in the light: {caption}."
        ],
        "Creative / Trending": [
            "Main character energy right here: {caption}!",
            "Certified mood: {caption}.",
            "Proof that ordinary life is extraordinary: {caption}.",
            "Living in this exact aesthetic right now — {caption}."
        ]
    }

    def __init__(self, model: BaseCaptionModel):
        self.model = model

    def _extract_tags(self, text: str, category: str) -> List[str]:
        """Extract meaningful visual keyword tags from model output."""
        words = re.findall(r"\b[A-Za-z]{3,}\b", text.lower())
        stopwords = {
            "the", "and", "with", "this", "that", "from", "into", "over", "under", "about",
            "there", "here", "some", "very", "photograph", "image", "picture", "standing",
            "sitting", "looking", "showing", "view", "close"
        }
        
        content_words = [w.capitalize() for w in words if w not in stopwords]
        
        # Add category context if not already present
        if category and category.capitalize() not in content_words:
            content_words.append(category.capitalize())

        # Ensure unique while preserving order
        unique_tags = list(dict.fromkeys(content_words))
        return unique_tags[:6] if unique_tags else ["VisionSpeak", "Aesthetic", "Visual"]

    def _generate_hashtags(self, tags: List[str], category: str, tone: str) -> List[str]:
        """Synthesize contextual hashtags based on detected tags and user tone."""
        tags_clean = [f"#{t.lower()}" for t in tags if t]
        defaults = [f"#{category.lower()}", f"#{tone.lower()}vibes", "#visionspeak", "#visualsoflife", "#photooftheday"]
        
        combined = list(dict.fromkeys(tags_clean + defaults))
        return combined[:5]

    def _pick_emoji(self, category: str, index: int = 0) -> str:
        """Select appropriate emoji."""
        bank = self.CATEGORY_EMOJIS.get(category, self.CATEGORY_EMOJIS["Other"])
        return bank[index % len(bank)]

    def generate_all_styles(
        self,
        image: Image.Image,
        category: str = "Other",
        tone: str = "Aesthetic"
    ) -> MultiStyleCaptionOutput:
        """
        Run real BLIP inference and produce 3 grounded Instagram captions,
        visual description, tags, and accessibility alt text.
        """
        start_time = time.perf_counter()

        # 1. Base unconditional inference to detect grounded scene contents
        base_res = self.model.generate(
            image,
            prompt=None,
            max_new_tokens=45,
            num_beams=3,
            repetition_penalty=1.35,
            style="base"
        )
        base_caption = base_res.caption.strip()

        # 2. Conditioned aesthetic inference
        aesthetic_prompt = f"a beautiful {category.lower()} photograph of" if category != "Other" else "a beautiful photograph of"
        aesthetic_res = self.model.generate(
            image,
            prompt=aesthetic_prompt,
            max_new_tokens=50,
            num_beams=4,
            repetition_penalty=1.3,
            style="aesthetic"
        )
        aesthetic_text = aesthetic_res.caption.strip()

        # 3. Creative / Emotional sampling inference
        emotional_res = self.model.generate(
            image,
            prompt="the atmosphere of",
            max_new_tokens=55,
            do_sample=True,
            temperature=0.75,
            top_p=0.9,
            repetition_penalty=1.3,
            style="emotional"
        )
        emotional_text = emotional_res.caption.strip()

        # Visual description
        description = f"Visual AI detected: {base_caption}."

        # Extract tags and hashtags
        tags = self._extract_tags(base_caption + " " + aesthetic_text, category)
        base_hashtags = self._generate_hashtags(tags, category, tone)

        # Format Style 1: Aesthetic
        emoji_1 = self._pick_emoji(category, 0)
        styled_1 = f"{aesthetic_text} {emoji_1}"

        # Format Style 2: Emotional
        emoji_2 = self._pick_emoji(category, 1)
        styled_2 = f"A quiet pause: {emotional_text} {emoji_2}"

        # Format Style 3: Creative / Trending
        emoji_3 = self._pick_emoji(category, 2)
        styled_3 = f"{base_caption} — completely unmatched aesthetic {emoji_3}"

        captions_payload = [
            {
                "id": 1,
                "style": "Aesthetic",
                "text": styled_1,
                "hashtags": base_hashtags
            },
            {
                "id": 2,
                "style": "Emotional",
                "text": styled_2,
                "hashtags": [f"#{t.replace('#', '')}" for t in base_hashtags[:3]] + ["#mindfulmoments", "#soulful"]
            },
            {
                "id": 3,
                "style": "Creative / Trending",
                "text": styled_3,
                "hashtags": [f"#{t.replace('#', '')}" for t in base_hashtags[:3]] + ["#instamood", "#trendingnow"]
            }
        ]

        total_elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        alt_text = f"Photo capturing {base_caption.lower()}."

        return MultiStyleCaptionOutput(
            description=description,
            tags=tags,
            captions=captions_payload,
            alt_text=alt_text,
            isRealAi=True,
            device=base_res.device,
            total_latency_ms=total_elapsed_ms,
            model_name=self.model.status().model_name,
            metadata={
                "base_latency_ms": base_res.generation_time_ms,
                "aesthetic_latency_ms": aesthetic_res.generation_time_ms,
                "emotional_latency_ms": emotional_res.generation_time_ms,
            }
        )
